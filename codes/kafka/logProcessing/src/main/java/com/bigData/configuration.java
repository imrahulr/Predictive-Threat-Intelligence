package com.bigData;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsConfig;

import java.util.Properties;

/**
 * Created by DELL on 16-Jan-19.
 */
public class configuration {



    private final Properties config;
    private String appId = "log-streamer";
    private String brokerIp = "192.168.75.132";
    private String brokerPort = "9092";
    private String autoOffsetReset = "earliest";
    private String maxByteBuffering = "0";
    private String inputTopicName = "log-json-input-130";
    private String outputTopicName = "output-json-stream";

    configuration()
    {

        config = new Properties();

        config.setProperty(StreamsConfig.APPLICATION_ID_CONFIG, appId);
        config.setProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, brokerIp+":"+brokerPort);
        config.setProperty(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        config.setProperty(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        config.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, autoOffsetReset);
        config.setProperty(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG,maxByteBuffering);



    }
    public String getInputTopicName()
    {
        return this.inputTopicName;
    }

    public String getOutputTopicName()
    {
        return this.outputTopicName;
    }

    public Properties getConfig()
    {
        Properties newProps = new Properties();
        config.forEach((key, value) -> {
            newProps.setProperty((String) key, (String) value);
        });
        return newProps;//new Properties(config);
    }








}
