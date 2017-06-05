package task1;
import task1.Map2;
import task1.Reduce2;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.filecache.DistributedCache;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;


public class newWordCount2 {
    public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
		if (otherArgs.length < 3) {
			System.err.println("Usage: ReplicationJoinDriver <inPlace> <inPhoto> <out> ");
			System.exit(2);
		}
		
		Job job = new Job(conf, "Replication Join");
		DistributedCache.addCacheFile(new Path(otherArgs[0]).toUri(),job.getConfiguration());
		job.setJarByClass(newWordCount2.class);
		job.setNumReduceTasks(3);
		job.setMapperClass(Map2.class);
		//job.setCombinerClass(combiner.class);
		job.setReducerClass(Reduce2.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);
		TextInputFormat.addInputPath(job, new Path(otherArgs[1]));
		TextOutputFormat.setOutputPath(job, new Path(otherArgs[2]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
		
    }
}