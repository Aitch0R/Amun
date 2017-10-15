package com.example.aitch.osi;

import android.content.Context;
import android.net.Uri;
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


public class Window extends Fragment {

    private Main main;
    private TCP tcp;
    private String address;
    private String name;

    private boolean auto;
    private String mode;
    private int level;
    Integer prog;

    View view;
    private TextView text_name;
    private CheckBox checkbox;
    private SeekBar bar;

    public Window() {}

    public void setup(Main main, TCP tcp, String pAddress, String[] info){
        this.main=main;
        this.tcp=tcp;
        address=pAddress+info[1]+",";
        name=info[2];
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
        view =  inflater.inflate(R.layout.fragment_window, container, false);
        bar = (SeekBar) view.findViewById(R.id.seekBar);
        text_name = (TextView) view.findViewById(R.id.objname);
        checkbox = (CheckBox) view.findViewById(R.id.checkBox);
        Log.d("test",Integer.toString(checkbox.getId()));

        text_name.setText(name);
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

        bar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
                bar.setSecondaryProgress(progress);
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
        return view;
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
    }

    private void setMode(boolean input){
        if (input){
            auto=true;
            mode="1";
            bar.setEnabled(false);
        }else{
            auto=false;
            mode="0";
            bar.setEnabled(true);
        }
    }

    private void sendStatus(){
        try {
            tcp.sendMessage(address+mode+','+level);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void process(String[] incoming){
        Log.d("light","id:"+"l");

        if (incoming[0].equals("1")){
            setMode(true);
            prog=Integer.parseInt(incoming[1]);
        }else{
            setMode(false);
            prog=(int)Math.sqrt(Integer.parseInt(incoming[1]));

        }
        checkbox.setChecked(auto);

        bar.setProgress(prog);

    }

    @Override
    public void onDetach() {
        super.onDetach();

    }


}
