package com.example.aitch.osi;

import android.app.Activity;
import android.app.Fragment;
import android.app.NotificationManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.app.FragmentManager;
import android.speech.RecognizerIntent;
import android.support.annotation.RequiresApi;
import android.support.design.widget.CoordinatorLayout;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.NotificationCompat;
import android.util.Log;
import android.view.SubMenu;
import android.view.View;

import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;

import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;
import android.widget.Toast;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.appindexing.Thing;
import com.google.android.gms.common.api.GoogleApiClient;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public class Main extends Activity implements NavigationView.OnNavigationItemSelectedListener {

    static CoordinatorLayout CoordinatorLayout;
    static NotificationCompat.Builder mBuilder;
    static NotificationManager mNotificationManager;
    static NavigationView navigationView;
    FragmentManager fragmentmanager;

    private Map<Integer,Fragment> frag_map=new HashMap();// <int,Fragment>;
    private Map<Integer,Room> rooms=new HashMap();
    private Menu menu;
    private SubMenu sm;

    private Fragment activefrag;
    private boolean set=false;
    private boolean apponscreen=true;



    TCP tcp = new TCP(this);
    Home main = new Home();
    Settings settings = new Settings();

    ADB fire = new ADB();

    private final int SPEECH_RECOGNITION_CODE = 1;//----------------------------------->
    private GoogleApiClient client;//--------------------------------------------------->

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        fragmentmanager = getFragmentManager();
        mNotificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        mBuilder = new NotificationCompat.Builder(this);
        setContentView(R.layout.main);
        CoordinatorLayout = (CoordinatorLayout) findViewById(R.id.fa);
        navigationView = (NavigationView) findViewById(R.id.nav_view); // must be defined after setContentView
        navigationView.setNavigationItemSelectedListener(this);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);

        if(savedInstanceState==null)
        {
            fragmentmanager.beginTransaction().add(R.id.main_content, settings).commit();
            //fragmentmanager.beginTransaction().add(R.id.main_content, settings).commit(); for blank room
            fragmentmanager.beginTransaction().add(R.id.main_content, main).commit();
            fragmentmanager.beginTransaction().hide(settings).commit();
            activefrag=main;
        }

        //DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();

        //setup frag_map
        frag_map.put(R.id.nav_main,main);
        frag_map.put(R.id.nav_blank,main);
        frag_map.put(R.id.nav_settings,settings);
        frag_map.put(R.id.nav_advanced,main);
        frag_map.put(R.id.nav_help,main);

        tcp.connect();
        tcp.startAutoReC();
        main.setup(this,tcp);
private void prereco(){
        startRecognition();
    }
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //startSpeechToText();
                // s,,,user,,,'id','name','address',,'objtype','objname','address',,'repeat,
                //String s="s,,,1,,,1,My room,1,,l,1,main light,,l,2,small light,,a,2,small light";
                //setup(s.split(",,,"));
                try {
                    tcp.sendMessage("s");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        menu=navigationView.getMenu();
        sm= menu.getItem(1).getSubMenu();
    }
    private void startSpeechToText() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT,
                "Speak something...");
        try {
            startActivityForResult(intent, SPEECH_RECOGNITION_CODE);
        } catch (ActivityNotFoundException a) {
            Toast.makeText(getApplicationContext(),
                    "Sorry! Speech recognition is not supported in this device.",
                    Toast.LENGTH_SHORT).show();
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
            case SPEECH_RECOGNITION_CODE: {
                if (resultCode == RESULT_OK && null != data) {
                    ArrayList<String> result = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                        String text = result.get(0);
                       // String text = "hi";
                    //main.txtOutput.setText(text);

                    if (text!=null) {
                        if (text.contains("ok")) {

                            try {
                                tcp.sendMessage("c,0,4,1,1,cr");
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }else if (text.contains("right")) {

                            try {
                                tcp.sendMessage("c,0,4,1,1,rt");
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }else if (text.contains("left")) {

                                try {
                                    tcp.sendMessage("c,0,4,1,1,lt");
                                } catch (IOException e) {
                                    e.printStackTrace();
                                }
                            Log.d("voice", "hi is wrong. sondern/"+text+"/");
                        }
                    }
                    Log.d("voice", "this is after");
                }
                break;
            }
        }
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();
        Log.e("here is the id", String.valueOf(id));
        fragmentmanager.beginTransaction().hide(activefrag).commit();
        activefrag=(Fragment)frag_map.get(id);
        fragmentmanager.beginTransaction().show(activefrag).commit();
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    void snack(String text){
        Snackbar snackbar = Snackbar.make(CoordinatorLayout, text, Snackbar.LENGTH_LONG);
        snackbar.show();
    }

    void notify(int id, String title, String text){
        if (apponscreen){
            Snackbar snackbar = Snackbar.make(CoordinatorLayout, text, Snackbar.LENGTH_LONG);
            snackbar.show();
        }else {
            mBuilder.setSmallIcon(R.drawable.common_google_signin_btn_icon_dark);
            mBuilder.setContentTitle(title);
            mBuilder.setContentText(text);
            mNotificationManager.notify(1, mBuilder.build());
        }
    }

    public void process (String cmd){
        String[] ncmd=cmd.split(",");
        int addr=Integer.parseInt(ncmd[0]);
        Room room;
        Log.d("process", "1");

        rooms.get(addr).process(Arrays.copyOfRange(ncmd,1,ncmd.length));
            //Home.process(Arrays.copyOfRange(cmd,1,cmd.length));
            //Log.d("prcess", "11");

        //room1.process(cmd);
    }

    public void setup(String[] info){
         /*
        roominfo
        s,,,'id','name','address',,'objtype','objname','address',,'repeat,
         */
        if (!set) {
            sm.clear();
            for (int i = 1; i < info.length; i++) {
                addroom(info[i]);
            }
        }
        try {
            tcp.sendMessage("u");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void addroom(String infostring){
        /*
        roominfo
        'id','name','address',,'objtype','objname','address',,'repeat,
        */
        String[] info=infostring.split(",,");
        String[] roominfo=info[0].split(",");
        int id=Integer.valueOf(roominfo[0]);
        String name=roominfo[1];
        Room n_room=new Room();
        rooms.put(id,n_room);
        fragmentmanager.beginTransaction().add(R.id.main_content, n_room).commit();
        fragmentmanager.beginTransaction().hide(n_room).commit();
        sm.add(R.id.room_group,id,id,roominfo[1].split(",")[0]);
        frag_map.put(id,n_room);
        invalidateOptionsMenu();
        n_room.inform(this,tcp,info);
    }

    //----------------------------------------------------------------------------------------

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.home, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Main/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    public Action getIndexApiAction() {
        Thing object = new Thing.Builder()
                .setName("Main Page") // TODO: Define a title for the content shown.
                // TODO: Make sure this auto-generated URL is correct.
                .setUrl(Uri.parse("http://[ENTER-YOUR-URL-HERE]"))
                .build();
            return new Action.Builder(Action.TYPE_VIEW)
                .setObject(object)
                .setActionStatus(Action.STATUS_TYPE_COMPLETED)
                .build();
    }
    @Override
    public void onPause(){
        super.onPause();
        apponscreen=false;
    }

    @Override
    public void onResume(){
        super.onResume();
        apponscreen=true;
    }

    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        AppIndex.AppIndexApi.start(client, getIndexApiAction());
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        AppIndex.AppIndexApi.end(client, getIndexApiAction());
        client.disconnect();
    }
}
