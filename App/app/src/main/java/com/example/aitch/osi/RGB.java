package com.example.aitch.osi;

import android.content.Context;

import android.os.Bundle;
import android.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;


public class RGB extends Light {

    private Main main;
    private TCP tcp;
    private String address;
    private String name;

    private boolean auto;
    private String mode;
    private int level;
    private int red;
    private int green;
    private int blue;

    View view;
    private TextView text_name;
    private CheckBox checkbox;
    private SeekBar levelBar;
    private SeekBar RBar;
    private SeekBar GBar;
    private SeekBar BBar;

    public RGB() {
        // Required empty public constructor
    }

    public void setup(Main main, TCP tcp, String pAddress, String[] info){
        this.main=main;
        this.tcp=tcp;
        address=pAddress+info[2]+",";
        name=info[3];
    }

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
        view = inflater.inflate(R.layout.fragment_rgb, container, false);

        levelBar = (SeekBar) view.findViewById(R.id.seekBarLevel);
        RBar = (SeekBar) view.findViewById(R.id.seekBarRed);
        GBar = (SeekBar) view.findViewById(R.id.seekBarGreen);
        BBar = (SeekBar) view.findViewById(R.id.seekBarBlue);

        text_name = (TextView) view.findViewById(R.id.objName);
        checkbox = (CheckBox) view.findViewById(R.id.checkBox);

        text_name.setText(name);

        levelBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                level=progress;
                sendStatus();
            }
        });

        checkbox.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (((CheckBox) v).isChecked()) {
                    setMode(true);
                }else{
                    setMode(false);
                }
                sendStatus();
            }
        });

        RBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                red=progress;
                sendStatus();
            }
        });

        GBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                green=progress;
                sendStatus();
            }
        });

        BBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                blue=progress;
                sendStatus();
            }
        });

        return view;
    }

    private void setMode(boolean input){
        if (input){
            auto=true;
            mode="1";
            levelBar.setMax(100);
            levelBar.setEnabled(false);
            RBar.setEnabled(false);
            GBar.setEnabled(false);
            BBar.setEnabled(false);
        }else{
            auto=false;
            mode="0";
            levelBar.setMax(10);
            levelBar.setEnabled(true);
            RBar.setEnabled(true);
            GBar.setEnabled(true);
            BBar.setEnabled(true);
        }
    }
    private void sendStatus(){
        try {
            tcp.sendMessage(address+','+mode+','+level+','+red+','+green+','+blue);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void process(String[] incoming){
        Log.d("light","id:"+"l");
        if (incoming[0].equals("1")){
            setMode(true);
        }else{
           setMode(false);
        }
        checkbox.setChecked(auto);
        levelBar.setProgress(Integer.parseInt(incoming[1]));
        RBar.setProgress(Integer.parseInt(incoming[2]));
        GBar.setProgress(Integer.parseInt(incoming[3]));
        BBar.setProgress(Integer.parseInt(incoming[4]));
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        if (context instanceof OnFragmentInteractionListener) {

        } else {
            throw new RuntimeException(context.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();

    }

    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name

    }
}
