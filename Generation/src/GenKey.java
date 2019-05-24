import java.io.*;

public class GenKey {

    public static void main(String[] args) throws IOException {

        //get the keys from the generated relations, each with 600 subfiles
        String iR = "/home/people/lcheng/storage/dbgen/customer.tbl.";
        String iS = "/home/people/lcheng/storage/dbgen/orders.tbl.";
        String oR = "/home/people/lcheng/storage/R/";
        String oS = "/home/people/lcheng/storage/S/";
        String strLine;
        String[] row;
        for (int i = 0; i < 600; i++) {
            String ifile = iR + (i + 1);
            String ofile = oR + i;
            FileInputStream istream = new FileInputStream(ifile);
            FileWriter owrite = new FileWriter(ofile);
            BufferedReader br = new BufferedReader(new InputStreamReader(istream));
            while ((strLine = br.readLine()) != null) {
                row = strLine.split("\\|");
                owrite.write(row[0] + "\n");
            }
            br.close();
            istream.close();
            owrite.flush();
            owrite.close();

            ifile = iS + (i + 1);
            ofile = oS + i;
            istream = new FileInputStream(ifile);
            owrite = new FileWriter(ofile);
            br = new BufferedReader(new InputStreamReader(istream));
            while ((strLine = br.readLine()) != null) {
                row = strLine.split("\\|");
                owrite.write(row[1] + "\n");
            }
            br.close();
            istream.close();
            owrite.flush();
            owrite.close();
        }
        System.out.println("The keys from relations have been extracted");
    }

}
