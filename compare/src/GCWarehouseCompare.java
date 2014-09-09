import java.io.File;
import java.awt.Desktop;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Iterator;
import java.util.Scanner;

import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CreationHelper;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;

public class GCWarehouseCompare {
	static File ourFile;
	static File warehouseFile;
	static PrintWriter writer;
	static int[] us, them;
	static boolean[] quantumBool, warehouseBool;
	static String[][] warehouseDetails, quantumDetails; 
	static int quantumFileLength, warehouseFileLength, warehouseNumCol,quantumFileColumnLength;
	static String fileName;

	public static void main(String[] args) throws IOException, ParseException {
		chooseFiles();

		us(); 
		
		warehouse();
		compare();
		write();
		Desktop dk=Desktop.getDesktop();
		dk.open(new File(fileName));
	}


	public static void write() throws IOException, ParseException{
		Workbook wb = new HSSFWorkbook();
		CreationHelper createHelper = wb.getCreationHelper();
		Sheet sheet = wb.createSheet("Only in Quantum");
		int rownum=0;

		for(int i = 0; i<quantumDetails.length;i++){
			if(!quantumBool[i]){
				Row row = sheet.createRow(rownum++);
				for(int j=0; j<quantumFileColumnLength;j++){
					row.createCell(j).setCellValue(quantumDetails[i][j]);
				}
			}
		}
		Sheet sheet2 = wb.createSheet("Only in warehouse");
		rownum =0;
		for(int i = 0; i<warehouseDetails.length;i++){
			if(!warehouseBool[i]){
				Row row = sheet2.createRow(rownum++);

				for(int j=0; j<warehouseNumCol; j++)
					row.createCell(j).setCellValue(warehouseDetails[i][j]);
			}
		}
		for(int i =0;i<quantumFileColumnLength;i++)
			sheet.autoSizeColumn(i);
		for(int i =0;i<warehouseNumCol;i++)
			sheet2.autoSizeColumn(i);
		DateFormat dateFormat = new SimpleDateFormat("MM.dd.yyyy");
		Calendar cal = Calendar.getInstance();
		String date = dateFormat.format(cal.getTime());
		fileName= date + "  Warehouse Quantum Comparison "+".xls";

		FileOutputStream fileOut = new FileOutputStream(fileName);
		wb.write(fileOut);
		fileOut.close();

	}

	public static void warehouse(){
		int count=0;
		try {
			System.out.println("hi");
			FileInputStream file = new FileInputStream(warehouseFile);

			//Get the workbook instance for XLS file 
			HSSFWorkbook workbook = new HSSFWorkbook(file);

			//Get first sheet from the workbook
			HSSFSheet sheet = workbook.getSheetAt(0);
			warehouseFileLength=sheet.getLastRowNum()+1;

			//Iterate through each rows from first sheet
			Iterator<Row> rowIterator = sheet.iterator();
			Row r =rowIterator.next();
			warehouseNumCol= r.getLastCellNum();
			them= new int[warehouseFileLength-1];


			while(rowIterator.hasNext()) {
				Row row = rowIterator.next();

				//For each row, iterate through each columns
				Iterator<Cell> cellIterator = row.cellIterator();
				while(cellIterator.hasNext()) {
					for(int x =0; x<4; x++)
						cellIterator.next(); 

					Cell cell = cellIterator.next();

					switch(cell.getCellType()) {
					case Cell.CELL_TYPE_BOOLEAN:
						break;
					case Cell.CELL_TYPE_NUMERIC:
						double x =cell.getNumericCellValue();
						them[count]= (int) x;
						//System.out.println(them[count]);
						count++;
						break;
					case Cell.CELL_TYPE_STRING:
						//String x= cell.getStringCellValue();
						//them[count]= Integer.parseInt(x);
						//System.out.println(x);
						//count++;
						break;

					}
					break;
				}
			}

			warehouseDetails= new String[warehouseFileLength][warehouseNumCol];





			file.close();


		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		detailsForwarehouse();





	}
	public static void detailsForwarehouse(){
		//Get the workbook instance for XLS file 
		HSSFWorkbook workbook;
		try {
			FileInputStream file = new FileInputStream(warehouseFile);
			workbook = new HSSFWorkbook(file);


			//Get first sheet from the workbook
			HSSFSheet sheet = workbook.getSheetAt(0);

			//Iterate through each rows from first sheet
			Iterator<Row> rowIterator = sheet.iterator();

			DateFormat df = new SimpleDateFormat("MM/dd/yyyy");
			int r=0;
			while(rowIterator.hasNext()) {
				Row row = rowIterator.next();

				//For each row, iterate through each columns


				for(int c =0; c<row.getLastCellNum();c++) {

					Cell cell = row.getCell(c, Row.RETURN_BLANK_AS_NULL);

					if(cell==null){

					}
					else if((c==2||c==8||c==9)&r>0){

						warehouseDetails[r][c]=df.format(cell.getDateCellValue());

					}
					else{

						switch(cell.getCellType()) {
						case Cell.CELL_TYPE_BOOLEAN:
							break;
						case Cell.CELL_TYPE_NUMERIC:
							String x=Integer.toString( (int) cell.getNumericCellValue());
							warehouseDetails[r][c]= x;

							break;
						case Cell.CELL_TYPE_STRING:
							String z= cell.getStringCellValue();
							warehouseDetails[r][c]= z;

							break;
						}
					}
				}
				r++;
			}
			file.close();


		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}



	}

	public static void detailsForQuantum() throws FileNotFoundException{
		Scanner test = new Scanner(ourFile).useDelimiter("\"");
		quantumFileColumnLength=0;
		while(!(test.next().equals("1"))){
			quantumFileColumnLength++;
		}
		quantumFileColumnLength/=2;
		//quantumFileColumnLength++;
		System.out.println(quantumFileColumnLength);
		test.close();
		quantumDetails= new String[quantumFileLength][quantumFileColumnLength];

		test = new Scanner(ourFile).useDelimiter("\"");

		for(int i = 0; i<quantumFileLength; i++){
			for(int j=0; j < quantumFileColumnLength; j++){
				if(test.hasNext()){
					quantumDetails[i][j]= test.next();}
				else
					break;
				if(test.hasNext()){
					test.next();}
				else
					break;

			}
		}

	}

	public static void compare(){
		warehouseBool = new boolean[warehouseDetails.length+1];
		warehouseBool[0]= false;

		for(int i =0; i <them.length;i++){
			warehouseBool[i+1] = false;
			for (int j = 0; j < us.length; j++) {
				if (them[i] == us[j]) {
					warehouseBool[i+1] = true;
					break;
				}
			}

		}
		quantumBool= new boolean[quantumDetails.length+1];
		quantumBool[0]= false;
		for(int i =0; i <us.length;i++){
			quantumBool[i+1]= false;
			for (int j = 0; j < them.length; j++) {
				if (us[i] == them[j]) {
					quantumBool[i+1] = true;
					break;
				}
			}



		}		
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

	public static void us() throws FileNotFoundException {
		Scanner test = new Scanner(ourFile).useDelimiter(",");
		quantumFileLength = 0;
		int invoiceCol =0;
		while(!(test.next().equals("\"Invoice No.\""))){
			invoiceCol++;
		}

		while (test.hasNextLine()) {// finds size of array
			test.nextLine();
			quantumFileLength++;
		}
		test.close();
		test = new Scanner(ourFile).useDelimiter(",");
		us = new int[quantumFileLength - 1];
		 
		int count = 0;

		test.nextLine();
		while (test.hasNextLine()) {//order number is always located at the second element in the line
			for(int i=0;i<invoiceCol;i++){
				test.next();
			}
			String x = test.next();
			x = x.substring(1, x.length() - 1);// trims the "" out of String
			us[count] = Integer.parseInt(x);//adds order number into the array
			//usdetails[count]= test.nextLine();
			test.nextLine();
			count++;

		}
		detailsForQuantum();

	}
}
