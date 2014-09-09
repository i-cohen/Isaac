package compare;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;


public class test {
	public static void main(String[] args) throws FileNotFoundException {
		// File us = new File("invoice.txt");
		int[] tmp = new int[150];
		int count = 0;
		File them = new File("110813b.txt");
		Scanner test = new Scanner(them).useDelimiter(",");
		test.nextLine();
		test.nextLine();
		test.nextLine();
		String x = test.next();
		System.out.println(test.next());
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
			//System.out.println(x+" "+ x.length());
			if(x.length()==6){
				tmp[count]=Integer.parseInt(x);
				count++;
			}
		}
		
	}
	
	
	/*
	 * for (int j = 0; j < 8; j++) test.nextLine(); while (test.hasNextLine()) {
	 * for (int j = 0; j < 7; j++){ if(test.hasNext()){ test.next(); } }
	 * if(!test.hasNext()) break; String x = test.next(); String y = ""; for
	 * (int i = 1; i < x.length(); i += 2) { y += x.substring(i, i + 1); }
	 * 
	 * int z = Integer.parseInt(y); System.out.println(z); tmp[count] = z;
	 * count++; test.nextLine(); test.nextLine(); }
	 */

}
