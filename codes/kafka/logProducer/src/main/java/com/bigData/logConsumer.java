package com.bigData;

/**
 * Created by DELL on 20-May-19.
 */

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mongodb.client.MongoCollection;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.*;
import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.connect.json.JsonSerializer;
import org.bson.Document;

import java.io.IOException;
import java.util.Collections;
import java.util.Properties;

public class logConsumer {


    public static void main(String[] args) {


        final Serializer<JsonNode> jsonSerializer = new JsonSerializer();
        final Deserializer<JsonNode> jsonDeserializer = new JsonDeserializer();
        final Serde<JsonNode> jsonSerde = Serdes.serdeFrom(jsonSerializer, jsonDeserializer);
        ;
        String topic = "output-json-stream";


        mgdb db = new mgdb();
        MongoCollection<Document> collection = db.getData("processed-logs");


        final Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,
                "192.168.75.132:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG,
                "KafkaExampleConsumer");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
                StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
                jsonDeserializer.getClass().getName());

        // Create the  using props.
        final Consumer<String,JsonNode> consumer =
                new KafkaConsumer<>(props);


        consumer.subscribe(Collections.singletonList(topic));


        final int giveUp = 100;
        int noRecordsCount = 0;

        while (true) {
            final ConsumerRecords<String, JsonNode> consumerRecords =
                    consumer.poll(1000);

            if (consumerRecords.count() == 0) {
                noRecordsCount++;
                if (noRecordsCount > giveUp) break;
                else continue;
            }

            consumerRecords.forEach(record -> {

                ObjectMapper mapper = new ObjectMapper();

                JsonNode node = record.value();

                String predictions = record.value().get("prediction").toString().replaceAll("\\\\","");


                try {
                    JsonNode array = mapper.readTree(predictions).get("");
                    System.out.println(array);
                } catch (IOException e) {
                    e.printStackTrace();
                }

                Document document = new Document("session",record.key())
                        .append("prediction", record.value().get("prediction").toString().replaceAll("\\\\",""))
                        .append("true", true);

                collection.insertOne(document);






                System.out.println(record.value().get("key")+"  "+record.value().get("prediction").toString().replaceAll("\\\\","")+"  "+record.value().get("offset"));





                consumer.commitAsync();
            });
            // consumer.close();
            System.out.println("DONE");


        }


    }}
