package src.usertag.test;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.atLeastOnce;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.junit.Test;

import task1.Map3;
/**
 * A simple unit test for TagMapper
 * it contains a single test method for valid record that 
 * emit one key value pair
 * @author Ying Zhou
 *
 */
public class TagMapperTest {
	@Test
	public void processValidRecord() throws IOException{
		Map3 tagMapper = new Map3();
		Text input = new Text("/Argentina/Autonomous+City+of+Buenos+Aires/Buenos+Aires	854	Dock+Sur	165");
		Mapper.Context context = mock(Mapper.Context.class);
		try{
		tagMapper.map(null, input, context);

		verify(context, atLeastOnce()).write(new Text("Argentina"), new Text("Buenos+Aires	854	Dock+Sur	165	"));

		
		}catch (Exception e){
			e.printStackTrace();
		}
	}

}
