package com.bigData.serialization.streamListSerializer;

import com.bigData.streamList;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

import java.util.Map;

/**
 * Created by DELL on 16-Jan-19.
 */
public class streamListSerde implements Serde<streamList> {
    private streamListSerializer ser;
    private streamListDeserializer des;

    public streamListSerde()
    {
        ser = new streamListSerializer();
        des = new streamListDeserializer();
    }
    @Override
    public void configure(Map<String, ?> map, boolean b) {


    }

    @Override
    public void close() {
        ser.close();
        des.close();

    }

    @Override
    public Serializer<streamList> serializer() {
        return ser;
    }

    @Override
    public Deserializer<streamList> deserializer() {
        return des;
    }
}
