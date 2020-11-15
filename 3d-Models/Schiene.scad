breite = 3; //Breite einer Schiene
laenge = 210; // Länger der Schiene insgesamt
abstand = 45;//Innenabstand der Schienen
hoehe = 7;
s_breite = 60;
s_hoehe = 2;
s_laenge = 10;
s_abstand = 30+s_laenge;
module schiene(){
    cube([breite, laenge, hoehe]);
}

module schweller(){
    cube([s_breite, s_laenge, s_hoehe]);
}

schiene();
translate([abstand + breite,0,0])schiene();
translate([0,s_abstand/2,0]){
    for(i = [0:s_abstand:laenge-s_abstand]){
        translate([-(s_breite-(abstand+2*breite))/2,i,0])schweller();
    }
}