package com.example.aitch.osi;

/**
 * Created by aitch on 12/26/16.
 */
import android.app.Activity;
import android.os.Handler;

import android.util.Log;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketException;
import java.util.Arrays;

 class TCP extends Activity {

    private Handler UIHandler= new Handler();
    private Handler ReConhandler = new Handler();
    private Socket socket = null;
    private Thread Thread1 = null;
    private DataOutputStream outToServer;
    private BufferedReader input;
    private boolean reconnect = true;

    private  int SERVERPORT = 1001; //Replace with your choice of PORT number
    private String SERVERIP = "192.168.0.10"; //Replace with your device IP address

    Main main;

    public TCP(Main main){
    this.main=main;
    }
    public void connect() {
        this.Thread1 = new Thread(new Thread1());
        this.Thread1.start();
    }

    class Thread1 implements Runnable {

        public void run() {

            try {
                Log.d("tcp", "0");
                InetAddress serverAddr = InetAddress.getByName(SERVERIP);
                socket = new Socket(serverAddr, SERVERPORT);
                outToServer = new DataOutputStream(socket.getOutputStream());
                Thread2 commThread = new Thread2();
                new Thread(commThread).start();
                UIHandler.post(new change(0,true));
                return;
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    class Thread2 implements Runnable {

        public Thread2() {
            try {
                input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void run() {

            while (!Thread.currentThread().isInterrupted()) {

                try {
                    String read = input.readLine();
                    if (read != null) {
                        UIHandler.post(new process(read));
                    } else {
                        Thread1 = new Thread(new Thread1());
                        Thread1.start();
                        return;
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }


        }

    }

    class process implements Runnable {
        private String msg;
        private String[] cmd;

        public process(String str) {
            this.msg = str;
        }
        @Override
        public void run() {
            this.cmd=msg.split(",,,");
            if(cmd[0].equals("s")){
                Log.d("setup text",msg);
                main.setup(Arrays.copyOfRange(cmd,1,cmd.length));
                Log.d("prcess", "s");
            }else if(cmd[0].equals("i")){
                main.process(cmd[1]);
                Log.d("prcess", "i");

            }
            main.notify(1,"title",msg);
        }
    }

    class change implements Runnable {
        private int nu;
        private boolean st;
        public change(int no,boolean state){
            nu=no;
            st=state;
        }
        public void run(){
            Home.idon(nu,st);

        }
    }

    public void sendMessage(String message) throws IOException {
        try{
            outToServer.writeBytes(message+"\n");
            outToServer.flush();
            Log.d("TCP", "Sent Message: " + message);
        }catch(NullPointerException|SocketException e){
            main.snack("Osiris client not connected to server");
            Home.idon(0,false);
            Log.e("TCP", "Sent Message: " + message);
        }
        if (main.equals(null)) {
            Log.e("null check", "is null");
        }else{
        //main.snack(message+"\n");
            }
    }

    public Runnable Concheck = new Runnable() {
        @Override
        public void run() {
            Log.d("TCP", "heartbeat" );
            try {
                outToServer.writeBytes("hb\n");
                outToServer.flush();
            } catch (NullPointerException | SocketException e) {
                Home.idon(0, false);
                if (reconnect) {
                    connect();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            ReConhandler.postDelayed(Concheck, 30000);

        }
    };

    public void startAutoReC(){
        reconnect = true;
        ReConhandler.post(Concheck);
    }

    public void stopAutoReC() {
        reconnect = false;
        ReConhandler.removeCallbacks(Concheck);
    }
}