import java.io.*;

public class VariousZipf {

    public static void main(String[] args) throws IOException {

        //add zipf
        double zipf = Double.parseDouble(args[0]);
        //the skew
        int skewness = 20;
        int N = 100;
        int P = 3 * N;
        int[][] matrix_R = new int[P][N];
        int[][] matrix_S = new int[P][N];
        int[] A_Skew = new int[N];  //the aggregation matrix
        int B = 600 / N; //the combined subfiles

        //get the keys from the generated relations
        String iR = "/home/people/lcheng/storage/R/";
        String iS = "/home/people/lcheng/storage/S/";
        String strLine;
        int key;
        int hv;
        for (int i = 0; i < N; i++) {  //the node i
            int start = i * B;
            int end = (i + 1) * B;
            for (int j = start; j < end; j++) {
                String ifile = iR + j;
                FileInputStream istream = new FileInputStream(ifile);
                BufferedReader br = new BufferedReader(new InputStreamReader(istream));
                while ((strLine = br.readLine()) != null) {
                    key = Integer.parseInt(strLine);
                    hv = key % P;
                    matrix_R[hv][i]++;
                }
                br.close();
                istream.close();

                ifile = iS + j;
                istream = new FileInputStream(ifile);
                br = new BufferedReader(new InputStreamReader(istream));
                while ((strLine = br.readLine()) != null) {
                    key = Integer.parseInt(strLine);
                    hv = key % P;
                    matrix_S[hv][i]++;
                }
                br.close();
                istream.close();
            }
        }

        //add zipf
        double[] prob = new double[N];
        ZipfGenerator zipfG = new ZipfGenerator(N, zipf);
        for (int i = 1; i <= N; i++) {
            prob[i - 1] = zipfG.getProbability(i);
        }

        //assign the size of each data chunk on each node based on the zipf distribution, for each row
        for (int j = 0; j < P; j++) { //for partition j
            int sum = 0;
            double size;
            int rest = 0;
            for (int i = 0; i < N; i++) {  //for node i
                sum += matrix_R[j][i];
            }

            for (int i = 0; i < N - 1; i++) {  //for node i
                size = sum * prob[i];
                matrix_R[j][i] = (int) size;
                rest += (int) size;
            }
            matrix_R[j][N - 1] = sum - rest;  //because the prob is in double, could some left, just put them on the final left.


            sum = 0;
            rest = 0;
            for (int i = 0; i < N; i++) {  //for node i
                sum += matrix_S[j][i];
            }

            for (int i = 0; i < N - 1; i++) {  //for node i
                size = sum * prob[i];
                matrix_S[j][i] = (int) size;
                rest += (int) size;
            }
            matrix_S[j][N - 1] = sum - rest;  //because the prob is in double, could some left, just put them on the final left.
        }

        //add skew
        for (int i = 0; i < N; i++) {  //for node i
            int diff;
            for (int j = 1; j < P; j++) {
                diff = matrix_R[j][i] * skewness / 100;
                A_Skew[i] += diff;
                matrix_R[j][i] -= diff;

                diff = matrix_S[j][i] * skewness / 100;
                A_Skew[i] += diff;
                matrix_S[j][i] -= diff;
            }
        }

        //just for output path
        int zipf1 = (int) (zipf * 10);

        //output matrix R, S and array_skew for further processing
        String ofile = "/home/people/lcheng/storage/GenData/zipf/" + zipf1 + "_R";
        FileWriter owrite = new FileWriter(ofile);
        for (int j = 0; j < P; j++) { //for partition j
            for (int i = 0; i < N - 1; i++) {
                owrite.write(matrix_R[j][i] + ",");
            }
            owrite.write(matrix_R[j][N - 1] + "\n");
        }
        owrite.flush();
        owrite.close();

        ofile = "/home/people/lcheng/storage/GenData/zipf/" + zipf1 + "_S";
        owrite = new FileWriter(ofile);
        for (int j = 0; j < P; j++) {
            for (int i = 0; i < N - 1; i++) {
                owrite.write(matrix_S[j][i] + ",");
            }
            owrite.write(matrix_S[j][N - 1] + "\n");
        }
        owrite.flush();
        owrite.close();

        ofile = "/home/people/lcheng/storage/GenData/zipf/" + zipf1 + "_A";
        owrite = new FileWriter(ofile);
        for (int i = 0; i < N - 1; i++) {
            owrite.write(A_Skew[i] + ",");
        }
        owrite.write(A_Skew[N - 1] + "\n");
        owrite.flush();
        owrite.close();

        System.out.println("The input data information has been generated for zipf " + zipf);

    }
}