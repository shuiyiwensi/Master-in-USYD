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
import task1.Driver;
import task1.Combiner;
import task1.filterdriver;
import task1.flitermap;


public class topfinddriver {
    public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
		if (otherArgs.length < 3) {
			System.err.println("Usage: ReplicationJoinDriver <inPlace> <inPhoto> <out> ");
			System.exit(2);
		}
		Path tmpFilterOut = new Path("/tmp/wtan4210output.txt");
		Job jointjob = new Job(conf, "Replication Join");
		DistributedCache.addCacheFile(new Path(otherArgs[0]).toUri(),jointjob.getConfiguration());
		jointjob.setJarByClass(Driver.class);
		jointjob.setNumReduceTasks(3);
		jointjob.setMapperClass(Map.class);
		jointjob.setReducerClass(Reduce.class);
		jointjob.setCombinerClass(Combiner.class);
		jointjob.setOutputKeyClass(Text.class);
		jointjob.setOutputValueClass(Text.class);
		TextInputFormat.addInputPath(jointjob, new Path(otherArgs[1]));
		TextOutputFormat.setOutputPath(jointjob,tmpFilterOut);
		jointjob.waitForCompletion(true);
		
		Job placeFilterJob = new Job(conf, "Place Filter");
		placeFilterJob.setJarByClass(filterdriver.class);
		placeFilterJob.setNumReduceTasks(1);
		placeFilterJob.setMapperClass(flitermap.class);
		placeFilterJob.setCombinerClass(filtercombiner.class);		
		placeFilterJob.setReducerClass(filterreduce.class);
		placeFilterJob.setOutputKeyClass(NullWritable.class);
		placeFilterJob.setOutputValueClass(Text.class);
		TextInputFormat.addInputPath(placeFilterJob, tmpFilterOut);
		TextOutputFormat.setOutputPath(placeFilterJob, new Path(otherArgs[2]));
		placeFilterJob.waitForCompletion(true);
		FileSystem.get(conf).delete(tmpFilterOut, true);
		
    }
}