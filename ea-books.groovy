/**
 * Найти документы adoc в дропбоксе с книгами,
 * отсортировать их по дате последней модификации
 * и скопировать на netlify
 */
 
publicFolder = 'public'
eaBooksFile = 'index.adoc'

/* На разных машинах каталоги Dropbox расположены по-разному.
 */
if (System.getProperty("os.name")=="Mac OS X") {
    dropboxFolder = "/Users/eabramovich/Dropbox/Public/books"
} else {
    dropboxFolder = "/home/egor/Dropbox/Public/books"
}

import javax.swing.JOptionPane;

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

printStatus("<html><h3>Копирование документов <br> из дропбокса с книгами на <code>netlify")
    
long tstr(tstamp) {
	return (tstamp-1550000000000)/100000
}

void debugList(noteList, delim) {
	noteList.each {
		println tstr(it.lastModified()) + " | " + it.path.substring(dropboxFolder.length()) 
	}
	println delim
}

/* В списке `bookList` будем сохранять последний timestamp для папки каждого месяца
 * и список заметок для этой папки.
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
    	for (afile in afiles) {
    		if (!afile.isFile()) continue;    	
    	    if (!afile.name.endsWith('.adoc')) continue;
    	    noteList << afile
    	}
    	if (noteList.size()>0) {
    		//debugList(noteList, "------")
    		noteList.sort { a,b -> a.lastModified() - b.lastModified() }
    		//debugList(noteList, "======")
    		tstamp = noteList[0].lastModified()
    		//println "     tstamp: " + tstr(tstamp)
    		bookList << [ tstamp: tstamp, notes: noteList, mdir: dir.name ]
    	}
    }
}

bookList.sort { a,b -> 
  if (a.tstamp > b.tstamp) return -1; 
  if (b.tstamp > a.tstamp) return 1;
  return 0;
}
//bookList.each { println it.mdir + " : " + tstr(it.tstamp)} // - 1555508398000 }

void writeToFile(f) {
	f.println "= Чтение по программированию"
	f.println ":toc: right"
	f.println ""
	for (book in bookList) {
		note = book.notes[0]
		tstamp = new Date(note.lastModified()).format("dd-MMM-yy")
		mstamp = note.parentFile.parentFile.name
		code = note.parentFile.name
		assert code.endsWith('_code')
		code = code.substring(0, code.length()-5)
		f.println "\n== ${code}\n"
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

printStatus("<html><h3>Документы из дропбокса с книгами &nbsp; <br> скопированы на <code>netlify")
