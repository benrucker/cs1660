import java.io.IOException;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.LongAdder;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TopN {
	public static final Log log = LogFactory.getLog(TopN.class);

	public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
		
		ConcurrentHashMap<String, LongAdder> counts = new ConcurrentHashMap<String, LongAdder>();

		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			StringTokenizer itr = new StringTokenizer(value.toString());
			String word;
			while (itr.hasMoreTokens()) {
				word = itr.nextElement().toString();
				counts.computeIfAbsent(word, k -> new LongAdder()).increment();
			}
		}

		@Override
		protected void cleanup(Context context) {
			// Create a list from elements of HashMap
	        List<Map.Entry<String, LongAdder> > list =
	               new LinkedList<Map.Entry<String, LongAdder> >(counts.entrySet());
	 
	        // Sort the list
	        Collections.sort(list, new Comparator<Map.Entry<String, LongAdder> >() {
	            public int compare(Map.Entry<String, LongAdder> o1,
	                               Map.Entry<String, LongAdder> o2)
	            {
	                return (int) -(o1.getValue().sum() - o2.getValue().sum());
	            }
	        });

			for (int i = 0; i < 5; i++) {
				try {
					context.write(new Text(list.get(i).getKey()),
								  new IntWritable(list.get(i).getValue().intValue()));
				} catch (IOException | InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}

	public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

		HashMap<String, Integer> counts = new HashMap<String, Integer>();

		public void reduce(Text key, Iterable<IntWritable> values, Context context)
				throws IOException, InterruptedException {
			int sum = 0;
			for (IntWritable val : values) {
				sum += val.get();
			}
			counts.put(key.toString(), sum);
		}

		@Override
		protected void cleanup(Context context) {
			// Create a list from elements of HashMap
	        List<Map.Entry<String, Integer> > list =
	               new LinkedList<Map.Entry<String, Integer> >(counts.entrySet());
	 
	        // Sort the list
	        Collections.sort(list, new Comparator<Map.Entry<String, Integer> >() {
	            public int compare(Map.Entry<String, Integer> o1,
	                               Map.Entry<String, Integer> o2)
	            {
	                return -(o1.getValue()).compareTo(o2.getValue());
	            }
	        });

			for (int i = 0; i < 5; i++) {
				try {
					context.write(new Text(list.get(i).getKey()),
								  new IntWritable(list.get(i).getValue()));
				} catch (IOException | InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "word count");
		job.setJarByClass(TopN.class);
		job.setMapperClass(TokenizerMapper.class);
		job.setCombinerClass(IntSumReducer.class);
		job.setReducerClass(IntSumReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		job.setNumReduceTasks(1);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}