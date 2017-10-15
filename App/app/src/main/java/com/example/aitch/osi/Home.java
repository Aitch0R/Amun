package com.example.aitch.osi;

import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.util.logging.Handler;


/**
 * A simple {@link Fragment} subclass.
 * Activities that contain this fragment must implement the
 * {@link Home.OnFragmentInteractionListener} interface
 * to handle interaction events.
 *
 * create an instance of this fragment.
 */
public class Home extends Fragment {
    private TCP tcp;
    public TextView txtOutput;
    static Context context;
    static Button[] ident=new Button[2];
    Main main;

    private OnFragmentInteractionListener mListener;


    public Home() {
        // Required empty public constructor
    }

    public void setup(Main main,TCP tcp){
        this.main = main;
        this.tcp=tcp;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        context=this.getActivity();


    }
View view;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        view=inflater.inflate(R.layout.fragment_home, container, false);
        // Inflate the layout for this fragment
        Button ra = (Button) view.findViewById(R.id.button);
        Button seth = (Button) view.findViewById(R.id.button2);

        final Button osirisid =(Button) view.findViewById(R.id.button15);
        ident[0]=osirisid;
        ident[1]=ra;

        txtOutput = (TextView) view.findViewById(R.id.textView2);

        ra.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
               /* try {
                   // tcp.sendMessage("p,ra");

                } catch (IOException e) {
                    e.printStackTrace();
                }*/
                main.notify(1,"hihihihi","d");
            }
        });
        seth.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    tcp.sendMessage("u");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        return view;
    }

    static void idon (int butno, boolean state){
        Button button=ident[butno];
        if (state){
            button.setTextColor( ContextCompat.getColor(context, R.color.accent_material_dark));
        }else{
            button.setTextColor( ContextCompat.getColor(context, R.color.foreground_material_dark));
        }
    }
    public static void process(String[] cmd){
        Log.d("prcess", "2");
        if (cmd[0].equals("ra")){
            Log.d("prcess", "2ra");
            int state = Integer.parseInt(cmd[1]);
            if(state==0){
                Log.d("prcess", "2ra0");
                idon(1,false);
            }else if(state==1){
                Log.d("prcess", "2ra1");
                idon(1,true);
            }
        }
    }

    public void onButtonPressed(Uri uri) {
        if (mListener != null) {
            mListener.onFragmentInteraction(uri);
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
