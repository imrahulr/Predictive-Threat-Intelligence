package com.bigData.serialization.streamListSerializer;

import com.bigData.streamList;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Deserializer;

import java.util.Map;

/**
 * Created by DELL on 16-Jan-19.
 */
public class streamListDeserializer implements Deserializer<streamList> {


    @Override
    public streamList deserialize(String arg0, byte[] devBytes) {
        ObjectMapper mapper = new ObjectMapper();
        streamList list = null;
        try {
            list = mapper.readValue(devBytes, streamList.class);
        } catch (Exception e) {

            e.printStackTrace();
            System.out.print("\n\n\n\n Exception occurred deserializer\n\n\n");
        }
        return list;
    }

    @Override
    public void close() {
        // TODO Auto-generated method stub

    }

    @Override
    public void configure(Map<String, ?> arg0, boolean arg1) {
        // TODO Auto-generated method stub

    }


}

