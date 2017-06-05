package task1;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.CharsetEncoder;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.filecache.DistributedCache;


public class Map extends Mapper<Object, Text, Text, Text> {
	private ArrayList<String> placetag=new ArrayList<String>();		//taglist
	private ArrayList<String> pureplaceidlist=new ArrayList<String>();
	private ArrayList<String> pureidtoplace=new ArrayList<String>();
	static CharsetEncoder asciiEncoder = Charset.forName("US-ASCII").newEncoder();
	private int numberofid;
	
	private void readline(String P) {
		// TODO Auto-generated method stub
System.out.println(P);
String[] placeArray = P.split("\t");
if(placeArray.length==7){
	int jud=Integer.parseInt(placeArray[5]);
	if(jud==22||jud==7){								
	//placeidlist.add(placeArray[0]);
	
	String[] placename = placeArray[6].split("/");
	int i=placename.length;
	if(jud==22){
		String placeulr="";					
		for(int j=1;j<=i-2;j++){
			placeulr=placeulr+"/"+placename[j];	
		}
		
		sort(placeArray[0],placeulr,pureplaceidlist,pureidtoplace);
	}
	else{String placeulr="";
	for(int j=1;j<=i-1;j++){
		placeulr=placeulr+"/"+placename[j];						
	}
	
	sort(placeArray[0],placeulr,pureplaceidlist,pureidtoplace);
	}
	}
}
	}
public int search(String a,int i, int j, ArrayList<String> b ){
int res;
int mid=(i+j)/2;
if(a.equals(b.get(mid))){res=mid; return res;}
if(j-i<=1){
	if(!(a.equals(b.get(i))||a.equals(b.get(j)))){
		res=-1;return res;}}
if(a.compareTo(b.get((i+j)/2))<0){return search(a,i,mid,b);}
else{return search(a,mid,j,b);}	

}	
	  public void setup(Context context) throws java.io.IOException, InterruptedException{
		    
		      
		      Path[] cacheFiles = DistributedCache.getLocalCacheFiles(context.getConfiguration());
		      if (null != cacheFiles && cacheFiles.length > 0) {		        		          
		            loadStopWords(cacheFiles);		           		        
		      }
		     
		  }

		public void loadStopWords(Path[] cachePath) throws IOException {
		    // note use of regular java.io methods here - this is a local file now
		    BufferedReader wordReader = new BufferedReader(new FileReader(cachePath[0].toString()));
		    try {
		      String line;
		      
		      //this.stopWords = new HashSet<String>();
		      while ((line = wordReader.readLine()) != null) {
		        readline(line);
		      }
		    } finally {
		      wordReader.close();
		    }
		  }





private Text word = new Text(),place=new Text();

public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
	
	String line = value.toString();
	
	String[] dataArray = line.toString().split("\t"); //split the data into array
	if (dataArray.length < 6){ //  record with incomplete data
		return; // don't emit anything
	}
	String tagString = dataArray[2];
	//String ownerString = dataArray[1];
	String placeidString = dataArray[4];
	String placename;
	String day=dataArray[3];
	
	int result=search(placeidString,0,numberofid,pureplaceidlist);	
	if(result!=-1){
	placename=pureidtoplace.get(result);
	

				tagString=settarget(tagString,placename,day);
				String placein=placename;
				place.set(placein);
				String tagString2="1"+"\t"+tagString;
				word.set(tagString2);
				context.write(place, word);
  }
} 
public static String settarget(String t, String q, String d){
	String a="";
	String Q=q;
	String[] placename=Q.split("/");
	ArrayList<String> placenames=new ArrayList<String>();
	ArrayList<String>placenames2=new ArrayList<String>();
	ArrayList<String>placenameskey=new ArrayList<String>();
	ArrayList<Integer>placenamelong=new ArrayList<Integer>();
	for(int i=1;i<placename.length;i++){
		if(placename[i].contains("+")){				
		String[] tmp=placename[i].split("\\+");
		int k=tmp.length;
		placenameskey.add(tmp[0]);
		placenamelong.add(k);
		placenames2.add(placename[i].replace("+"," "));
		placenames.add(placename[i].replace("+",""));}
		else{
			placenames.add(placename[i]);
		}
	}
	String[] D=d.split("-");		
	String[] T=t.split(" ");
	
	for(int i=0;i<T.length;i++){
		int jud=0; 
		if(T[i].equals(D[0])){jud=1;}
		else{
		for(String wordp:placenames){
			if(T[i].equalsIgnoreCase(wordp.trim())){jud=1;}
			else{
				for(int k=0;k<placenameskey.size();k++){
				if(T[i].equalsIgnoreCase(placenameskey.get(k))&&(T.length-1-i)>=placenamelong.get(k)){						
					String namelong="";
					for(int l=0;l<placenamelong.get(k);l++){
						namelong=namelong+T[i+l]+" ";
					}
					if(placenames2.get(k).equalsIgnoreCase(namelong.trim())){
						jud=1;
						i=i+placenamelong.get(k)-1;
					}
				}
			}					
			}
			}			
		}
		if(jud==0){
			a=a+T[i]+" 1 ";}
	}
	return a;
}

	public void sortdetal(String a, int i, int j,ArrayList<String> b,ArrayList<String> d,String c){
	int mid=(i+j)/2;
	if(a.compareTo(b.get(mid))==0){return;}
	if(j-i<=1){
		if(a.compareTo(b.get(mid))>0){
			b.add(i+1,a);d.add(i+1,c);numberofid=numberofid+1;return;}else{
				b.add(i,a);d.add(i,c);numberofid=numberofid+1;return;}}
	if(a.compareTo(b.get((i+j)/2))<0){sortdetal(a,i,mid,b,d,c);}
	else{sortdetal(a,mid,j,b,d,c);}
	}
	public void sort(String a,String c,ArrayList<String> b,ArrayList<String> d){
	if(numberofid==0){
		b.add(a);
		d.add(c);
		numberofid=numberofid+1;
	}else{
	sortdetal(a,0,b.size(),b,d,c);
	}}
}


