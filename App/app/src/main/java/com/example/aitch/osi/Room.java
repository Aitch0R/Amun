package com.example.aitch.osi;

import android.app.FragmentManager;
import android.os.Bundle;
import android.app.Fragment;
import android.util.Log;
import android.util.SparseArray;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.GridLayout;
import android.widget.SeekBar;
import android.widget.TextView;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Room extends Fragment {

    final private String lightId="2";
    final private String windowId="3";
    final private String irid="4";
    final private String adbId="5";
    private int frameCount=1;

    private Main main;
    private TCP tcp;

    private String[] info;

    private Map<Integer,Light> Lights= new HashMap<>();
    private Map<Integer,Window> Windows= new HashMap<>();
    private Map<Integer,ADB> ADBs= new HashMap<>();

    private String name;
    private String address;

    private String autoBright;
    private String sub;
    private int tBright;


    private boolean autoTemp;
    private int tTemp;

    private View view;
    private TextView textname;
    private TextView textbright;
    private TextView texttemp;
    private SeekBar seekbrightness;
    private SeekBar seekweight;
    private SeekBar seektemperature;
    private CheckBox chkautobright;
    private CheckBox chkautotemp;



    public Room() {}

    private void setup(int[] frames) {
        //l,1,main light,,l,2,small light
        int objid;
        for (int i=1;i<info.length;i++){
            String[] obj_info=info[i].split(",");

            if(obj_info[0].equals("l")) {
                if (obj_info[1].equals("1")) {
                    Light light = new Light();
                    objid = Integer.valueOf(obj_info[2]);
                    Lights.put(objid, light);
                    light.setup(main, tcp, address + lightId + ",", obj_info);
                    getChildFragmentManager().beginTransaction().add(frames[frameCount], Lights.get(objid)).commit();
                } else if (obj_info[1].equals("2")) {
                    RGB rgb = new RGB();
                    objid = Integer.valueOf(obj_info[2]);
                    Lights.put(objid, rgb);
                    rgb.setup(main, tcp, address + lightId + ",", obj_info);
                    getChildFragmentManager().beginTransaction().add(frames[frameCount], Lights.get(objid)).commit();
                }
            }else if(obj_info[0].equals("w")){
                Window window = new Window();
                objid = Integer.valueOf(obj_info[1]);
                Windows.put(objid, window);
                window.setup(main, tcp, address + windowId + ",", obj_info);
                getChildFragmentManager().beginTransaction().add(frames[frameCount], Windows.get(objid)).commit();
            }else  if(obj_info[0].equals("a")) {
                ADB adb = new ADB();
                objid=Integer.valueOf(obj_info[1]);
                ADBs.put(objid, adb);
                adb.setup(main, tcp, address+adbId+",", obj_info);
                getChildFragmentManager().beginTransaction().add(frames[frameCount], ADBs.get(objid)).commit();

            }else  if(obj_info[0].equals("ir")) {
                if (obj_info[1].equals("tv")) {
                    TV tv = new TV();
                    tv.setup(main, tcp, address + irid + ",", obj_info);
                    getChildFragmentManager().beginTransaction().add(frames[frameCount], tv).commit();
                }
            }
            frameCount++;
        }
    }

    public void inform(Main main, TCP tcp, String[] info) {
         /*
        roominfo
        'id','name',,'objtype','objid','objname','address',,'repeat,
         */
        this.main=main;
        this.tcp=tcp;
        this.info=info;
        String[] roominfo=info[0].split(",");
        name=roominfo[1];
        address="c,"+roominfo[0]+",";
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (savedInstanceState == null) {

        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        view= inflater.inflate(R.layout.fragment_room, container, false);


        textname = (TextView) view.findViewById(R.id.textViewname);
        textbright = (TextView) view.findViewById(R.id.textView3);
        texttemp = (TextView) view.findViewById(R.id.textView9);
        seekbrightness = (SeekBar) view.findViewById(R.id.seekBarbrightness);
        seektemperature = (SeekBar) view.findViewById(R.id.seekBartemperature);
        chkautobright = (CheckBox) view.findViewById(R.id.checkBoxbrightness);
        chkautotemp = (CheckBox) view.findViewById(R.id.checkBoxtemperature);
        int[] frames={0,R.id.frame1,R.id.frame2,R.id.frame3,R.id.frame4,R.id.frame5,R.id.frame6}; //smarter?
        setup(frames);

        chkautobright.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (((CheckBox) v).isChecked()) {
                    autoBright="1";
                }else{
                    autoBright="0";
                }
            }
        });

       chkautotemp.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (((CheckBox) v).isChecked()) {
                    mautotemp(true,true);
                    seektemperature.setClickable(true);
                }else{
                    mautotemp(false,true);
                    seektemperature.setClickable(false);
                }
            }
        });

        seekbrightness.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                tBright=progress;
            }
        });


        seektemperature.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progress;
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                this.progress = progress;
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                tTemp=progress;
            }
        });

        return view;
    }

    public void mautotemp (boolean state,boolean set){
        autoTemp=state;
        if (set) {
            String value;
            if (autoTemp){value="1";
            }else{value="0";}
            totcp("0,1,s," + value);

        }else{
            chkautotemp.setChecked(state);
        }
    }

    private void mtemp(int lvl, boolean set){
        tTemp=lvl;
        if (set){totcp("0,1,t,"+tTemp);}
        else{seekbrightness.setProgress(tTemp);}
    }

    private void bRegStatus() {

        try {
            tcp.sendMessage(address+"0,1,"+autoBright+","+sub+","+tBright);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void tRegStatus() {

        try {
            tcp.sendMessage(address+"0,1,"+autoTemp+","+tTemp);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void totcp(String msg){
        try {
            tcp.sendMessage(address+msg);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void process(String[] input){
        int index=Integer.parseInt(input[0]);
        if (index==0) {//actual,mode,mode,target
            int reg=Integer.parseInt(input[1]);

            int mode=Integer.parseInt(input[3]);
            int type=Integer.parseInt(input[1]);

            if (reg==0) {
                textbright.setText(input[2]);
                if (mode == 0) {
                    autoTemp=false;
                } else {
                    autoTemp=true;
                }
                seekbrightness.setProgress(Integer.parseInt(input[4]));
                chkautobright.setChecked(true);

            }else if (reg==1) {
                Log.d("temp reg", input[2]);
                if (input[2].equals("a")) {
                    texttemp.setText(input[3]);
                } else if (input[2].equals("t")) {
                    mtemp(mode, false);
                } else if (input[2].equals("s")) {
                    if (mode == 0) {
                        mautotemp(false, false);
                    } else {
                        mautotemp(true, false);
                    }

                }
            }


        }
        if (index==2) {
            Log.d("light index",input[1]);
            Lights.get(Integer.parseInt(input[1])).process(Arrays.copyOfRange(input,2,input.length));
        }else if (index==3){


        }else if (index==44){
             //windows.get(Integer.parseInt(input[1])).process(input);

        }else if (index==3){
            //media.get(Integer.parseInt(input[1])).process(input);

    }

    }
}