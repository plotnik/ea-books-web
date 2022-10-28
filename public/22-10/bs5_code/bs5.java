///usr/bin/env jbang "$0" "$@" ; exit $?
//DEPS info.picocli:picocli:4.6.3

import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Parameters;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;
import java.util.concurrent.Callable;

import static java.lang.System.*;

@Command(name = "bs5", mixinStandardHelpOptions = true, version = "1.0", 
         description = "Update Bootstrap 5 version in HTML file and trim tags if necessary.")
class bs5 implements Callable<Integer> {

    @Parameters(index = "0", description = "Input file.")
    File inputFile;

    @Override
    public Integer call() throws Exception { 
        if (!inputFile.exists()) {
            out.println("[ERROR] File not found: " + inputFile.getPath());
            return 1;
        }

        String text = StrUtils.loadStr(inputFile.getPath());
        
        text = trimTokens(text);
        text = updateBootstrapVersion(text);
        
        String outName = inputFile.getPath();
        //outName = outName.substring(0, outName.length() - ".html".length()) + "~.html";
        StrUtils.saveStr(outName, text);
        out.println("File created: " + outName);

        return 0;
    }

    String updateBootstrapVersion(String text) {
        XmlTokenizer tok = new XmlTokenizer(text);
        StringBuilder result = new StringBuilder();
        while (tok.hasNext()) {
            String word = tok.next();
            if (tok.inTag()) {
                boolean closing = word.startsWith("</");
                word = word.substring(closing ? 2 : 1, word.length() - 1).trim();
                word = (closing ? "</" : "<") + word + ">";
                //out.println("|" + word + "|");
            }
            result.append(word);
        }
        return result.toString();
    }

    /**
     * Converts
     *   < h1 >Bootstrap Container</ h1 >
     * into
     *   <h1>Bootstrap Container</h1>
     */
    String trimTokens(String text) {
        XmlTokenizer tok = new XmlTokenizer(text);
        StringBuilder result = new StringBuilder();
        while (tok.hasNext()) {
            String word = tok.next();
            if (tok.inTag()) {
                if (word.contains("/bootstrap.min.css")) {
                    word = "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\">";                  
                }
                if (word.contains("/bootstrap.bundle.min.js")) {
                    word = "<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js\">";
                }
            }
            result.append(word);
        }
        return result.toString();
    }

    public static void main(String... args) {
        int exitCode = new CommandLine(new bs5()).execute(args);
        System.exit(exitCode);
    }
}

class StrUtils {

    /**
     * Load string from file, Java 11.
     * @see https://howtodoinjava.com/java/io/java-read-file-to-string-examples/#example-1-reading-the-complete-file-into-a-string
     */
    static String loadStr(String fname) {
        try {
            return Files.readString(Path.of(fname));
        } catch (IOException e) {
            return null;
        }
    }

    /** 
     * Save string to file. 
     */
    public static void saveStr(String fname, String text)
            throws IOException {
        PrintWriter out = new PrintWriter(new FileOutputStream(fname));
        out.print(text);
        out.close();
    }
}

class XmlTokenizer implements Iterator<String> {

    String text;
    int curPos;
    boolean tag;
    StringBuffer result;

    public XmlTokenizer(String text) {
        this.text = text;
        result = new StringBuffer();
    }

    @Override
    public boolean hasNext() {
        return curPos < text.length();
    }

    @Override
    public String next() {
        result.setLength(0);
        while (curPos < text.length()) {
            char ch = text.charAt(curPos++);
            if (tag) {
                result.append(ch);
                if (ch == '>') {
                    tag = false;
                    break;
                }
            } else { // not tag
                if (ch == '<') {
                    tag = true;
                    curPos--;
                    break;
                }
                result.append(ch);
            }
        }
        return result.toString();
    }

    public boolean inTag() {
        return !tag;
    }

}
