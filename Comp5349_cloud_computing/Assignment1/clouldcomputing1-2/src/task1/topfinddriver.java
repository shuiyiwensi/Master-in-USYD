package task1;
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.filecache.DistributedCache;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import task1.Map;
import task1.Reduce;
import task1.newWordCount;
import task1.Map2;
import task1.Reduce2;
import task1.newWordCount2;
import task1.Map3;
import task1.Reduce3;
import task1.newWordCount3;

public class topfinddriver {
    public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
		if (otherArgs.length < 3) {
			System.err.println("Usage: ReplicationJoinDriver <inPlace> <inPhoto> <out> ");
			System.exit(2);
		}
		Path tmpFilterOut = new Path("/tmp/wtan4210output1.txt");
		Path tmpFilterOut2 = new Path("/tmp/wtan4210output2.txt");
		Job jointjob = new Job(conf, "Replication Join");
		DistributedCache.addCacheFile(new Path(otherArgs[0]).toUri(),jointjob.getConfiguration());
		jointjob.setJarByClass(newWordCount.class);
		jointjob.setNumReduceTasks(3);
		jointjob.setMapperClass(Map.class);
		jointjob.setReducerClass(Reduce.class);
		jointjob.setOutputKeyClass(Text.class);
		jointjob.setOutputValueClass(Text.class);
		TextInputFormat.addInputPath(jointjob, new Path(otherArgs[1]));
		TextOutputFormat.setOutputPath(jointjob,tmpFilterOut);
		jointjob.waitForCompletion(true);
		
		Job placeFilterJob = new Job(conf, "Place Filter");
		placeFilterJob.setJarByClass(newWordCount2.class);
		placeFilterJob.setNumReduceTasks(3);
		placeFilterJob.setMapperClass(Map2.class);
		placeFilterJob.setReducerClass(Reduce2.class);
		placeFilterJob.setOutputKeyClass(Text.class);
		placeFilterJob.setOutputValueClass(Text.class);
		TextInputFormat.addInputPath(placeFilterJob, tmpFilterOut);
		TextOutputFormat.setOutputPath(placeFilterJob,tmpFilterOut2);
		placeFilterJob.waitForCompletion(true);
		FileSystem.get(conf).delete(tmpFilterOut, true);
		
		Job placeFilterJob2 = new Job(conf, "Place Filter");
		placeFilterJob2.setJarByClass(newWordCount3.class);		
		placeFilterJob2.setMapperClass(Map3.class);
		placeFilterJob2.setReducerClass(Reduce3.class);
		placeFilterJob2.setOutputKeyClass(Text.class);
		placeFilterJob2.setOutputValueClass(Text.class);
		TextInputFormat.addInputPath(placeFilterJob2, tmpFilterOut2);
		TextOutputFormat.setOutputPath(placeFilterJob2, new Path(otherArgs[2]));
		placeFilterJob2.waitForCompletion(true);
		FileSystem.get(conf).delete(tmpFilterOut2, true);
		
    }
}