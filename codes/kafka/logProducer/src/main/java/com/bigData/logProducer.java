package com.bigData;

import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.bson.Document;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Created by DELL on 20-May-19.
 */
public class logProducer {

    static String topic = "log-json-input-130";
    static Map<String,Integer> offset = new HashMap<>();



    public static void main(String[] args) {


        Properties properties = new Properties();

        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,"192.168.75.132:9092");
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.ACKS_CONFIG,"all");
        properties.setProperty(ProducerConfig.RETRIES_CONFIG,"3");
        properties.setProperty(ProducerConfig.LINGER_MS_CONFIG,"1");
        properties.setProperty(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG,"true");



        Producer<String,String> producer = new KafkaProducer<>(properties);

        int i=0;


        mgdb db = new mgdb();

        MongoCollection<Document> collection = db.getData("raw-logs");

        MongoCursor<Document> cursor = collection.find().iterator();

        try {
            while (cursor.hasNext()) {
                Document temp = cursor.next();

                String session = temp.get("session").toString();
                String eventid = temp.get("eventid").toString();
                String timestamp = temp.get("timestamp").toString();

                System.out.println(temp);


                try{

                    producer.send(produce(session,topic,eventid,timestamp));

                }
                catch (Exception e)
                {
                    break;
                }


            }
        } finally {
            cursor.close();
        }

    }

    private static ProducerRecord<String,String> newRandomTransaction(String name)
    {
        ObjectNode transaction = JsonNodeFactory.instance.objectNode();
        Integer amount = ThreadLocalRandom.current().nextInt(0,100);
        Instant now = Instant.now();
        transaction.put("name",name);
        transaction.put("amount",amount);
        transaction.put("time",now.toString());
        return new ProducerRecord<String, String>("bank-transaction11",name,transaction.toString());


    }





    private static ProducerRecord<String,String> produce (String sessId,String topic,String eventid,String timestamp)

    {




        ObjectNode transaction = JsonNodeFactory.instance.objectNode();


        //Instant now = Instant.now();
        transaction.put("sessId",sessId);
        transaction.put("timestamp",timestamp);
        transaction.put("event_id",eventid);

        if (!offset.containsKey(sessId))
        {
            offset.put(sessId,0);
        }
        else
        {
            offset.put(sessId,offset.get(sessId)+1);
        }
        transaction.put("offset",offset.get(sessId));

        System.out.println(transaction.get("offset") + " " + transaction.get("sessId"));
        return new ProducerRecord<String, String>(topic,sessId,transaction.toString());




    }










}
