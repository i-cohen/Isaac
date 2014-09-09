import java.io.File;
import java.awt.Desktop;

import javax.swing.JOptionPane;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Scanner;

import javax.swing.JFileChooser;
public class WarehouseQuantumCompare {
	static File ourFile;
	static File warehouseFile;
	static PrintWriter writer;
	static int[] us, them;
	static String[] usdetails, themdetails;
	static int quantumFileLength, warehouseFileLength;

	public static void main(String[] args) throws IOException {
		chooseFiles(); // requests Warehouse and Quantum files to use.
		DateFormat dateFormat = new SimpleDateFormat("MM.dd.yyyy");
		Calendar cal = Calendar.getInstance();
		String date = dateFormat.format(cal.getTime());
		String x= date + "  Warehouse Quantum Compare "+".txt";
		writer = new PrintWriter(x,
				"UTF-8"); // output file name

		us(); // scans quantum file and puts all order numbers in array us
		them(); // scans warehouse file and puts all order numbers in array them
		compare(); // compares both files and writes the output to the file
		// above.
		//File file = new File("out.txt");
		Desktop dk=Desktop.getDesktop();
		dk.open(new File(x));

	}

	public static void compare() {
		writer.println("These are the ones that are not entered in the warehouse system:");
		for (int i = 0; i < us.length; i++) {// does an exhaustive search to
			// find orders only in quantum
			boolean ok = false;
			for (int j = 0; j < them.length; j++) {
				if (us[i] == them[j]) {
					ok = true;
					break;
				}
			}
			if (!ok){
				writer.print(us[i]);
				writer.println(usdetails[i]);

			}

		}
		writer.println();
		writer.println("These are the ones that are not entered in quantum:");
		for (int i = 0; i < them.length; i++) {// does an exhaustive search to
			// find orders only in warehouse
			boolean ok = false;
			for (int j = 0; j < us.length; j++) {
				if (them[i] == us[j]) {
					ok = true;
					break;
				}
			}
			if (!ok){
				writer.print(them[i]);
				writer.println(themdetails[i]);
			}

		}
		writer.close();

	}

	public static void chooseFiles() {
		// asks for files
		final JFileChooser fc = new JFileChooser();
		JOptionPane.showMessageDialog(null, "Please Select Quantum File");
		int returnval = fc.showOpenDialog(null);
		ourFile = fc.getSelectedFile();
		JOptionPane.showMessageDialog(null, "Please Select Warehouse File");
		returnval = fc.showOpenDialog(null);
		warehouseFile = fc.getSelectedFile();

	}

	public static void them() throws FileNotFoundException {
		warehouseFileLength=0;
		//int[] tmp = new int[1000];

		//String[] tmpString= new String[1000]; 
		Scanner test = new Scanner(warehouseFile).useDelimiter(",");
		test.nextLine();
		while(test.hasNextLine()){
			while(test.hasNext()){
				if (test.next().equals("JDE Associates"))
					warehouseFileLength++;
				break;
			}
		}


		test = new Scanner(warehouseFile).useDelimiter(",");
		themdetails= new String[warehouseFileLength];
		them = new int[warehouseFileLength];
		int count = 0;
		//consumes file in a weird way. Once the file reaches String "JDE Associates" it consumes 3 more elements to get the id number
		String x = test.next();
		while (test.hasNextLine()) {
			while (test.hasNext()) {

				if (x.equals("JDE Associates"))
					break;
				else
					x = test.next();
			}
			for (int i = 0; i < 3; i++)
				if (test.hasNext())
					x = test.next();

			if (x.length() == 6) {//assures that the value is a 6 digit number
				them[count] = Integer.parseInt(x);// adds to array
				themdetails[count]= test.nextLine();
				count++;
			}
		}
		//		themdetails= new String[count]; 
		//		them = new int[count];//creates array with correct size
		//		for (int i = 0; i < them.length; i++) {
		//			them[i] = tmp[i];
		//			themdetails[i]=tmpString[i];
		//
		//		}

	}

	public static void us() throws FileNotFoundException {
		Scanner test = new Scanner(ourFile).useDelimiter(",");
		quantumFileLength = 0;
		int column =0;
		while(!(test.next().equals("\"Invoice No.\""))){
			column++;
		}
		while (test.hasNextLine()) {// finds size of array
			test.nextLine();
			quantumFileLength++;
		}

		test = new Scanner(ourFile).useDelimiter(",");
		us = new int[quantumFileLength - 1];
		usdetails = new String[quantumFileLength-1]; 
		int count = 0;

		test.nextLine();
		while (test.hasNextLine()) {//order number is always located at the second element in the line
			for(int i=0;i<column;i++){
				test.next();
			}
			String x = test.next();
			x = x.substring(1, x.length() - 1);// trims the "" out of String
			us[count] = Integer.parseInt(x);//adds order number into the array
			usdetails[count]= test.nextLine();
			count++;

		}

	}

}
