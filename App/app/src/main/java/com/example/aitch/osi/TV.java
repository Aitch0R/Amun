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
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;

public class TV extends Fragment {
    private Main main;
    private TCP tcp;
    private String address;
    private String tempadd;
    private String name;

    View view;


    public void setup(Main main, TCP tcp, String pAddress, String[] info){
        this.main=main;
        this.tcp=tcp;
        address=pAddress+info[2]+",0,";
        tempadd=pAddress+info[2]+",1,";
        name=info[3];

    }
    private OnFragmentInteractionListener mListener;

    public TV() {}


    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {

        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        view= inflater.inflate(R.layout.fragment_tv, container, false);
        Button power=(Button) view.findViewById(R.id.button17);
        Button mute=(Button) view.findViewById(R.id.button18);
        Button menu=(Button) view.findViewById(R.id.button25);
        Button source=(Button) view.findViewById(R.id.button24);
        Button up=(Button) view.findViewById(R.id.button19);
        Button down=(Button) view.findViewById(R.id.button20);
        Button right=(Button) view.findViewById(R.id.button22);
        Button left=(Button) view.findViewById(R.id.button23);
        Button ok=(Button) view.findViewById(R.id.button21);
        Button volUp=(Button) view.findViewById(R.id.button26);
        Button volDn=(Button) view.findViewById(R.id.button27);
        Button chUp=(Button) view.findViewById(R.id.button28);
        Button chDn=(Button) view.findViewById(R.id.button29);
        Button exit=(Button) view.findViewById(R.id.button30);
        TextView text_name = (TextView) view.findViewById(R.id.objname);
        CheckBox conon=(CheckBox) view.findViewById(R.id.checkBox3);
        text_name.setText(name);

        power.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("power");
            }
        });
        mute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("mute");
            }
        });
        menu.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("menu");
            }
        });
        source.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("source");
            }
        });
        up.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("up");
            }
        });
        down.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("down");
            }
        });
        ok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("ok");
            }
        });
        right.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("right");
            }
        });
        left.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("left");
            }
        });
        chUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("chup");
            }
        });
        chDn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("chdn");
            }
        });
        volUp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("volup");
            }
        });
        volDn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("voldn");
            }
        });
        exit.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                totcp("exit");
            }
        });


        conon.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (((CheckBox) v).isChecked()) {
                    try {
                        tcp.sendMessage(tempadd+"1");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }else{
                    try {
                        tcp.sendMessage(tempadd+"0");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
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
        if (context instanceof OnFragmentInteractionListener) {
            mListener = (OnFragmentInteractionListener) context;
        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        void onFragmentInteraction(Uri uri);
    }
}
