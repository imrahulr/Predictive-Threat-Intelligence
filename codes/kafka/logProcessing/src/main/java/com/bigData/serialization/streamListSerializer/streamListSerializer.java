package com.bigData.serialization.streamListSerializer;

import com.bigData.streamList;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serializer;

import java.util.Map;

/**
 * Created by DELL on 16-Jan-19.
 */
public class streamListSerializer implements Serializer<streamList> {


    @Override
    public byte[] serialize(String arg0, streamList list) {
        byte[] serializedBytes = null;
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            serializedBytes = objectMapper.writeValueAsString(list).getBytes();
        } catch (Exception e) {
            e.printStackTrace();

          //  System.out.print("\n\n\n\n Exception occurred \n\n\n");
        }
        return serializedBytes;
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
