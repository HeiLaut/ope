include <BOSL/constants.scad>
use <BOSL/masks.scad>

achsbreite = 60;
achsradius = 2.1;
rad_dia = 36;
radstand = 20.5; //Abstand Rad - Aussenkante
radbreite = 3;
abstand = 10; //Abstand Rad-Chassie

rand = 1;
p_x = 73.2;
p_y = 11.5;
p_z = 148.2;
wagenlaenge = p_z+2*rand;
$fn = 80;

module radaufhaengung(){
    module schnitt(){
    resize([wagenlaenge+1,rad_dia/2,achsbreite+2])linear_extrude(achsbreite+2)import("schnitt.svg", convexity=3);
    }

    *translate([-rad_dia, rad_dia/4,150-20])rotate([0,90,0])cylinder(d = rad_dia, h=2);
    union(){
        //Randbleche
        difference(){
           union(){ 
                translate([0,-rad_dia/3,0])linear_extrude(rand)square([achsbreite,rad_dia/3],center = true);
                translate([0,-rad_dia/3,wagenlaenge-rand])linear_extrude(rand)square([achsbreite,rad_dia/3],center = true);
                }
            
        translate([0,-rad_dia/3,-1])cylinder(d = 4.2, h = p_z/2);
              }           
        //Seitenteile 
        difference(){
        linear_extrude(wagenlaenge)
        difference(){
            square([achsbreite,rad_dia],center = true);
            translate([0,rand])square([achsbreite-rand*2,rad_dia], center = true);
        }
        translate([-rad_dia, rad_dia/4,0.16*wagenlaenge])rotate([0,90,0])cylinder(r = achsradius, h = 70);
        *translate([-rad_dia,30,wagenlaenge/2])rotate([0,90,0])cylinder(h = 70, d = 70);
        translate([-rad_dia, rad_dia/4,0.84*wagenlaenge])rotate([0,90,0])cylinder(r = achsradius, h = 70);
        translate([0,0,wagenlaenge/2])scale([0.7,1,1])rotate([90,0,0])cylinder(d = p_x/1.3, h = 20);
        translate([achsbreite/2,rad_dia/2+0.5,wagenlaenge+0.5])rotate([180,90,0])schnitt();
        }
        //Druckstütze
        *translate([0,-rad_dia/3,wagenlaenge-2*rand-0.8])linear_extrude(0.7)square([achsbreite,rad_dia/3],center = true);
    }
}
module phone_holder(){
    
    mirror([0,1,0])
    translate([0,(p_y+2*rand)/2,(p_z+2*rand)/2])
    difference(){
    cube([p_x+2*rand,p_y+2*rand,p_z+2*rand],center = true);
    cube([p_x,p_y,p_z],center = true);
    translate([0,rand*2,5/2])cube([p_x,p_y+4,p_z-5], center = true);
    scale([1,0.6,1])translate([-(p_x+2*rand)/2,p_z-rand*8,rand*4])rotate([0,90,0])cylinder(r = p_z, h =(p_x+2*rand), $fn = 80);
     rotate([90,0,0])cylinder(d = p_x/1.3, h = 20); //Aussparung Mite
    }
    
    
}

module rad(){
     d2 = 29.4;
     h1 = 2;
     h2 = 4.8;
     h3 = 2.5;
    difference(){
        union(){
            cylinder(d1 = rad_dia, d2 = d2, h  = h1);
            translate([0,0,2])cylinder(d = d2, h = h2);
            translate([0,0,h1+h2])cylinder(h = h3, d = 6.3);
        }
        cylinder(h = h1+h2+h3+1, r = achsradius);
    }    
}   
module radstand(){
    h = 40;
    d = 6.4;
    difference(){
        cylinder(d = d, h = h);
        cylinder(r = achsradius, h = h+1);
    }
}
*radstand();
*rad();

schnitt();
translate([0,-rad_dia/2+rand,0])phone_holder();
radaufhaengung();
