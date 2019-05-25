package com.bigData;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.connect.json.JsonSerializer;
import com.bigData.serialization.streamListSerializer.streamListSerde;

import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

/**
 * Created by DELL on 16-Jan-19.
 */
public class Utils {

    final Serializer<JsonNode> jsonSerializer;// = new JsonSerializer();
    final Deserializer<JsonNode> jsonDeserializer;// = new JsonDeserializer();
    final Serde<JsonNode> jsonSerde;// = Serdes.serdeFrom(jsonSerializer,jsonDeserializer);

    final String [] events = {"null","cowrie.client.size", "cowrie.client.version", "cowrie.command.failed","cowrie.command.input/delete", "cowrie.command.input/dir_sudo", "cowrie.command.input/other",
            "cowrie.command.input/system", "cowrie.command.input/write", "cowrie.command.success",
            "cowrie.direct-tcpip.data", "cowrie.direct-tcpip.request", "cowrie.log.closed",
            "cowrie.log.open", "cowrie.login.failed", "cowrie.login.success", "cowrie.session.closed",
            "cowrie.session.connect", "cowrie.session.file_download", "cowrie.session.input"};


    final Map<String,Integer> map = new HashMap<>();

    Utils()
    {
        jsonSerializer = new JsonSerializer();
        jsonDeserializer = new JsonDeserializer();
        jsonSerde = Serdes.serdeFrom(jsonSerializer, jsonDeserializer);

        for (int i=0;i<events.length;i++)
        {
            map.put(events[i],i);
        }

    }

    public String reverseMap(int i)
    {
        if(i<events.length)
        return events[i];

        return null;
    }

    public int map(String key)
    {
        return map.get(key);
    }


    public Serde<JsonNode> getJsonSerde()
    {
        return jsonSerde;
    }

    public streamListSerde getstreamListSerde()
    {
        return new streamListSerde();
    }




    public ObjectNode createArray(ObjectNode node1)  {

        try {
            ObjectMapper mapper = new ObjectMapper();
            ObjectNode node = (ObjectNode)node1;
            //ObjectNode node1 = (ObjectNode) new ObjectMapper().putPOJO(node);

            //node.putPOJO(node1.t);
            int[] arr = {};
            ArrayNode array = mapper.valueToTree(arr);
            node.putArray("array").addAll(array);
            return node1;
        }
        catch (Exception e)
        {

        }
        return null;

    }

    public ObjectNode createArray(ObjectNode node1,int [] a)
    {
        ObjectNode node = (ObjectNode)node1;
        ObjectMapper mapper = new ObjectMapper();
        int[] arr = a;
        ArrayNode array = mapper.valueToTree(arr);
        node.putArray("array").addAll(array);

        return node;
    }

    public  ObjectNode addToArray(JsonNode node1,int element) throws IOException {
        ObjectMapper mapper = new ObjectMapper();

        ObjectNode node = (ObjectNode)node1;
        //JsonNode array = mapper.readTree(node.toString()).get("data");

        try {
            JsonNode array = mapper.readTree(node.toString()).get("array");
            List<Integer> l1 = new LinkedList<>();


            int count = array.size()+1;
            if (array.isArray()) {
                for (final JsonNode objNode : array) {


                    if(count >10)
                    {
                        count--;
                        continue;
                    }
                    l1.add((int)objNode.asInt());
                    System.out.println(objNode);
                }

            }
            l1.add(element);



            //int[] a = l1.stream().mapToInt(i->i).toArray();

            node = createArray(node, l1.stream().mapToInt(i->i).toArray());         /////////  ***




        } catch (IOException e) {
            e.printStackTrace();
        }

        // node.putArray("array").addAll(array);

        return node;
    }



    public  ObjectNode addToArray(ObjectNode node1,int[] elements) throws IOException {
        ObjectMapper mapper = new ObjectMapper();

        //JsonNode array = mapper.readTree(node.toString()).get("data");

        ObjectNode node = (ObjectNode)node1;
        try {
            JsonNode array = mapper.readTree(node.toString()).get("array");


            List<Integer> l1 = new LinkedList<>();

            int count = array.size()+elements.length;
            if (array.isArray()) {
                for (final JsonNode objNode : array) {


                    l1.add((int)objNode.asInt());
                    //      System.out.println(objNode);
                }

            }


            for(int i:elements) {
                l1.add(i);

            }



            //int[] a = l1.stream().mapToInt(i->i).toArray();

            node = createArray(node, l1.stream().mapToInt(i->i).toArray());         /////////  ***




        } catch (IOException e) {
            e.printStackTrace();
        }

        // node.putArray("array").addAll(array);

        return node;
    }




    public  ObjectNode addToArray(ObjectNode node1,List<Integer> l2) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode node = (ObjectNode)node1;
        node = createArray(node, l2.stream().mapToInt(i->i).toArray());         /////////  ***
        return node;
    }



    public int[] toIntArray(List<Integer> list){
        int[] ret = new int[list.size()];
        for(int i = 0;i < ret.length;i++)
            ret[i] = list.get(i);
        return ret;
    }












}
