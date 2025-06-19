FB Prompts Xml
==============

Sync Firebase "prompts" collection with XML file.

::

  import argparse
  import xml.etree.ElementTree as ET
  from datetime import datetime, timezone
  import dateutil.parser

  import firebase_admin
  from firebase_admin import credentials, firestore


  def parse_args():
      parser = argparse.ArgumentParser(
          description="Synchronize Firebase 'prompts' collection with an XML file"
      )
      parser.add_argument(
          '--xml', '-x', required=True,
          help='Path to the XML file'
      )
      parser.add_argument(
          '--service-account', '-s', required=True,
          help='Path to your Firebase service account JSON'
      )
      return parser.parse_args()


  def parse_iso(dt_str):
      """Parse an ISO8601 string into a timezone-aware datetime."""
      return dateutil.parser.isoparse(dt_str)


  def fmt_iso(dt):
      """Format a datetime as ISO8601 in UTC."""
      return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


  def load_xml(path):
      tree = ET.parse(path)
      root = tree.getroot()
      records = {}
      now = datetime.now(timezone.utc)
      for elem in root.findall('prompt'):
          name = elem.findtext('name')
          note = elem.findtext('note') or ''
          tags = [t.text for t in elem.findall('tags/tag')]

          created_el = elem.find('created_at')
          created_at = parse_iso(created_el.text) if created_el is not None else now

          updated_el = elem.find('updated_at')
          if updated_el is not None:
              updated_at = parse_iso(updated_el.text)
          else:
              # if missing, treat as now
              updated_at = now
              # add the missing node
              updated_el = ET.SubElement(elem, 'updated_at')
              updated_el.text = fmt_iso(now)

          records[name] = {
              'elem': elem,
              'note': note,
              'tags': tags,
              'created_at': created_at,
              'updated_at': updated_at
          }
      return tree, root, records


  def load_firebase(db):
      docs = db.collection('prompts').stream()
      records = {}
      for doc in docs:
          data = doc.to_dict()
          name = data.get('name')
          if not name:
              continue
          ca = data.get('created_at')
          ua = data.get('updated_at')
          records[name] = {
              'ref': db.collection('prompts').document(doc.id),
              'note': data.get('note', ''),
              'tags': data.get('tags', []),
              'created_at': ca if isinstance(ca, datetime) else now,
              'updated_at': ua if isinstance(ua, datetime) else now
          }
      return records


  def sync(tree, root, xml_recs, fb_recs):
      now = datetime.now(timezone.utc)

      all_names = set(xml_recs) | set(fb_recs)
      for name in all_names:
          xml = xml_recs.get(name)
          fb = fb_recs.get(name)

          # exists both
          if xml and fb:
              if fb['updated_at'] > xml['updated_at']:
                  # Firebase is newer -> update XML
                  elem = xml['elem']
                  elem.find('note').text = fb['note']
                  tags_el = elem.find('tags')
                  # clear tags
                  for t in tags_el.findall('tag'):
                      tags_el.remove(t)
                  # add tags
                  for tag in fb['tags']:
                      t_el = ET.SubElement(tags_el, 'tag')
                      t_el.text = tag
                  # update timestamps
                  elem.find('updated_at').text = fmt_iso(fb['updated_at'])

              elif xml['updated_at'] > fb['updated_at']:
                  # XML is newer -> update Firebase
                  fb['ref'].update({
                      'note': xml['note'],
                      'tags': xml['tags'],
                      'updated_at': xml['updated_at']
                  })

          # only in XML -> create in Firebase
          elif xml and not fb:
              data = {
                  'name': name,
                  'note': xml['note'],
                  'tags': xml['tags'],
                  'created_at': xml['created_at'],
                  'updated_at': xml['updated_at']
              }
              db.collection('prompts').add(data)

          # only in Firebase -> add to XML
          elif fb and not xml:
              elem = ET.SubElement(root, 'prompt')
              ET.SubElement(elem, 'name').text = name
              ET.SubElement(elem, 'note').text = fb['note']
              tags_el = ET.SubElement(elem, 'tags')
              for tag in fb['tags']:
                  t_el = ET.SubElement(tags_el, 'tag')
                  t_el.text = tag
              ET.SubElement(elem, 'created_at').text = fmt_iso(fb['created_at'])
              ET.SubElement(elem, 'updated_at').text = fmt_iso(fb['updated_at'])

      # write back XML
      ET.indent(tree, space="  ", level=0)
      tree.write(args.xml, encoding="utf-8", xml_declaration=True)


  if __name__ == '__main__':
      args = parse_args()
      # init Firebase
      cred = credentials.Certificate(args.service_account)
      firebase_admin.initialize_app(cred)
      db = firestore.client()

      tree, root, xml_recs = load_xml(args.xml)
      fb_recs = load_firebase(db)
      sync(tree, root, xml_recs, fb_recs)
      print(f"Synchronized Firebase and XML file: {args.xml}")
