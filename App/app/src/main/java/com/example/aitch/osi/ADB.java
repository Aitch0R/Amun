package com.example.aitch.osi;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import java.io.IOException;

public class ADB extends Fragment {

    private Main main;
    private TCP tcp;
    private String address;
    private String name;

    public ADB() {
        // Required empty public constructor
    }

    public void setup(Main main,TCP tcp,String pAddress, String[] info){
        this.main=main;
        this.tcp=tcp;
        this.address= pAddress+info[1]+",";
        name=info[2];
    }

    View view;


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(final LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        view =inflater.inflate(R.layout.fragment_adb, container, false);
        Button ok= (Button) view.findViewById(R.id.button3);
        Button up= (Button) view.findViewById(R.id.button4);
        Button left= (Button) view.findViewById(R.id.button5);
        Button right= (Button) view.findViewById(R.id.button6);
        Button down= (Button) view.findViewById(R.id.button7);
        Button back= (Button) view.findViewById(R.id.button8);
        Button home= (Button) view.findViewById(R.id.button9);
        Button menu= (Button) view.findViewById(R.id.button10);
        Button bw= (Button) view.findViewById(R.id.button11);
        Button pp= (Button) view.findViewById(R.id.button12);
        Button fw= (Button) view.findViewById(R.id.button13);
        Button send= (Button) view.findViewById(R.id.button14);
        final EditText inputtxt=(EditText) view.findViewById(R.id.editText);

        ok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,center");
            }
        });
        up.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,up");
            }
        });
        left.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,left");
            }
        });
        right.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,right");
            }
        });
        down.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,down");
            }
        });
        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,back");
            }
        });
        home.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,home");
            }
        });
        menu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,menu");
            }
        });
        bw.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,dn");
            }
        });
        pp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                    totcp("1,dn");
            }
        });
        fw.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("1,dn");
            }
        });
        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("2,"+inputtxt.getText());
            }
        });

        return view;
    }
    private void totcp(String msg){
        try {
            tcp.sendMessage(address+msg);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    @Override
    public void onDetach() {
        super.onDetach();
    }
}
