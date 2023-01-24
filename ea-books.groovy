/**
 * Найти документы adoc в дропбоксе с книгами,
 * отсортировать их по дате последней модификации
 * и скопировать на netlify
 */

@Grab('info.picocli:picocli-groovy:4.6.0')
import static picocli.CommandLine.*
import groovy.transform.Field

@Command(name = 'ea-books', mixinStandardHelpOptions = true, version = '2022-12-22',
  description = 'Generate book index for Netlify.')
@picocli.groovy.PicocliScript

/* На разных машинах каталоги Dropbox расположены по-разному.
 */
@Parameters(index = '0', description = 'Dropbox folder.')
@Field String dropboxFolder

@Option(names = ['-f'], description = 'Public folder.')
@Field publicFolder = 'public'

@Option(names = ['-o'], description = 'Index file to generate.')
@Field eaBooksFile = 'index.adoc'

@Option(names = ['--verbose'], description = 'Verbose info on specified folder.')
@Field String verboseFolder = ''

import javax.swing.JOptionPane;
import groovy.ant.AntBuilder;

useSwing = false

/* В зависимости от настроек мы можем выводить сообщения о текущем статусе
 * в свинговое окошко либо на консоль.
 */
void printStatus(String msg) {
	if (useSwing) {
        JOptionPane.showMessageDialog(null, msg, "ea-books", 1);
	} else {
		println msg
	}
}

printStatus("Generate book index for Netlify")
    
long tstr(tstamp) {
	return (tstamp-1550000000000)/100000
}

/** 
 * Распечатать список документов с датами, найденный для указанной папки. 
 * @param noteList  List of File
 * @param delim     Напечатать разделитель
 */
void debugList(noteList, delim) {
    noteList.each {
	    String path = it.path.substring(dropboxFolder.length());
		println tstr(it.lastModified()) + " | " + path
	}
	println delim
}

/* В списке `bookList` будем сохранять последний timestamp для папки каждого месяца
   и список заметок для этой папки.
   
   Можно потом переписать на java
   Listing a Directory's Contents
   https://docs.oracle.com/javase/tutorial/essential/io/dirs.html#listdir
 */
bookList = []
dirs = new File(dropboxFolder).listFiles()
for (dir in dirs) {
    
    /* Пройдемся по дропбоксу и выделим свои папки формата `ГГ-ММ`
     * с разбивкой по месяцам.
     */
    if (!dir.isDirectory()) continue;
    if (!(dir.name ==~ /\d{2}-\d{2}/)) continue;
    
    subdirs = dir.listFiles()
    for (subdir in subdirs) {
    	if (!subdir.isDirectory()) continue;
    	if (!subdir.name.endsWith('_code')) continue;
    	
    	/* Для указанного месяца найдем папки с заметками
    	 * и сохраним имена файлов заметок в `noteList`.
    	 */
    	noteList = []
    	afiles = subdir.listFiles()
    	quotes = false
    	for (afile in afiles) {
    		if (!afile.isFile()) continue; 
    		if (afile.name.equals('quotes.html')) quotes = true;
    	    if (!afile.name.endsWith('.adoc')) continue;
    	    noteList << afile
    	}
    	if (noteList.size()>0) {
            /* Отсортировать документы в папке по дате, более новые сверху.
             */
            boolean showDebugInfo = verboseFolder == dir.name
            if (showDebugInfo) {
                debugList(noteList, "-------------------^ before sort")
            }
            noteList.sort { a,b -> 
              if (b.lastModified() > a.lastModified()) {
                  return 1
              } else 
              if (b.lastModified() < a.lastModified()) {
                  return -1
              } else {
                  return 0
              }
            }
            // TODO: можно перевести этот скрипт на jbang, а то разность между 
            //       двумя числами long как-то не очень в groovy работает...
            //noteList.sort { a,b -> b.lastModified() - a.lastModified() }
            /*
            noteList.sort { a,b -> 
                long result = a.lastModified() - b.lastModified();
                if (showDebugInfo) {
                    println "a: ${tstr(a.lastModified())} ${a.name} | b: ${tstr(b.lastModified())} ${b.name} | result: $result"
                }
                return result;
            } */
            if (showDebugInfo) {
                debugList(noteList, "===================^ after sort")
            }
                
            /* Выбрать самую свежую дату файла документа и присвоить ее текущей папке 
             */
            tstamp = noteList[0].lastModified()
            if (showDebugInfo) {
                println "-------------------^ tstamp result: " + tstr(tstamp)
            }
    		bookList << [ tstamp: tstamp, notes: noteList, mdir: dir.name, quotes: quotes ]
    	}
    }
}

bookList.sort { a,b -> 
  if (a.tstamp > b.tstamp) return -1; 
  if (b.tstamp > a.tstamp) return 1;
  return 0;
}

bookList.each { 
    if (verboseFolder==it.mdir) {
        println it.mdir + " : " + tstr(it.tstamp)
    }
}


void writeToFile(f) {
	f.println "= Чтение по программированию"
	f.println ":icons: font"
	f.println ":toc: right"
	f.println ""
	for (book in bookList) {
		note = book.notes[0]
		tstamp = new Date(note.lastModified()).format("dd-MMM-yy")
		mstamp = note.parentFile.parentFile.name
		code = note.parentFile.name
		assert code.endsWith('_code')
		code = code.substring(0, code.length()-5)
		quotes = ""
		if (book.quotes) {
		    quotes = "icon:bookmark[]"
		}
		f.println "\n== ${quotes} ${code}\n"
		f.println "${mstamp}, изменение: ${tstamp}\n"  
		for (note in book.notes) {
			assert note.name.endsWith('.adoc')
			name = note.name.substring(0, note.name.length()-5)
			f.println "- link:${mstamp}/${code}_code/${name}.html[${name}]" 
		}		
	}
}

String htmlName(adocName) {
	assert adocName.endsWith('.adoc')
	return adocName.substring(0,adocName.length()-5) + '.html'
}

f = new File(publicFolder, eaBooksFile).newWriter()
writeToFile(f)
f.close()
"asciidoctor $publicFolder/$eaBooksFile".execute()
println "$eaBooksFile created and processed"

def ant = new AntBuilder()
for (book in bookList) {
	for (note in book.notes) {
		docName = note.path.substring(dropboxFolder.length()+1)
		//println htmlName(docName)
		ant.copy(todir: publicFolder) {
			fileset(dir: dropboxFolder) {
				include(name: docName)
				include(name: htmlName(docName))
			}
		}
	}
}

printStatus("Dropbox documents copied to Netlify folder")
