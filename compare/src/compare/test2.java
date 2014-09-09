package compare;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class test2 {
	
	
	
	public static void main(String[] args) throws FileNotFoundException {
		File us = new File("invoice.txt");
		int[] tmp = new int[150];
		int count = 0;
		Scanner test = new Scanner(us).useDelimiter(",|\\n");
		System.out.println(test.nextLine());
		/*
		
		System.out.println(test.nextLine());
		while(test.hasNextLine()){
			
		String x = test.next();
		x= x.substring(1,x.length()-1);
		tmp[count]= Integer.parseInt(x);
		System.out.println(tmp[count]);
		count++;
		test.nextLine();
		}
		
		*/
	}
}