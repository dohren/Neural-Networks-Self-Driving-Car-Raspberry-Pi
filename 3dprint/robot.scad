

module base_plate() {
    translate ([-80, -45, 0]) polygon(points=[
        [15, 0],
        [160 - 15, 0],
        [160, 5],
        [160, 90 - 5],
        [160 - 15, 90],
        [15, 90],
        [0, 90 - 15],
        [0, 15]
    ], paths=[[0, 1, 2, 3, 4, 5, 6, 7]]);
}

module motor() {
    linear_extrude(19) 
        polygon(points=[
            [0, 0],           
            [23, 0],    
            [23, 32],      
            [18, 37],      
            [5, 37],   
            [0, 32]         
        ]);
    
    difference() {
      rotate([90, 0, 0]) translate([11.5, 9.2, 5.5])      
        cylinder(h = 12, r = 11.5, center = true);
      translate([0, -14, -3]) cube([23, 16, 3]);  
      translate([0, -14, 19]) cube([23, 16, 3]);   
    }
    
    difference() {
      rotate([90, 0, 0]) translate([11.5, 9.7, 16])      
        cylinder(h = 8.5, r = 10, center = true);
      translate([0, -21, -1]) cube([23, 10, 2]);  
      translate([0, -21, 18]) cube([23, 10, 2]);   
    }
    
    difference() {
        translate([12, -21, 9.5]) sphere(d = 15);
        translate([0, -30, 0]) cube([23, 5, 23]); 
   }
   
   rotate([0, 0, 90]) translate([26, -11.6, 9])      
        cylinder(h = 37, r = 3, center = true);


   translate([-5, 0, -3.]) cube([35, 10, 3]);
   translate([-5, 0, -22]) cube([3, 10, 22]);
}

module battery() {
   translate([60, 0, 28]) cube ([44, 92, 23], center= true);
   translate([75, 19, 3]) cylinder(h = 15, r = 2.5);
   translate([55, 19, 3]) cylinder(h = 15, r = 2.5);
   translate([75, -17, 3]) cylinder(h = 15, r = 2.5);
   translate([55, -17, 3]) cylinder(h = 15, r = 2.5);
}

module motor_shield() {
   translate([0, 0, 18]) cube ([44, 43, 3], center = true);
   translate([17, 0, 30]) cube ([10, 23, 24], center = true);
   translate([14, -12, 30]) cube ([16, 1, 24], center = true);
   translate([14, 12, 30]) cube ([16, 1, 24], center = true);
   
   translate([-7, 17, 23]) cube ([10, 8, 8], center = true); 
   translate([-7, -17, 23]) cube ([10, 8, 8], center = true); 
   translate([-17, 6, 23]) cube ([8, 15, 8], center = true);
    
   translate([0, 7, 23]) cylinder(h = 12, r = 4, center = true);
   translate([-10, -7, 23]) cylinder(h = 12, r = 4, center = true);
    
   translate([17, 17, 3]) cylinder(h = 15, r = 2.5);
   translate([-17, 17, 3]) cylinder(h = 15, r = 2.5);
   translate([17, -17, 3]) cylinder(h = 15, r = 2.5);
   translate([-17, -17, 3]) cylinder(h = 15, r = 2.5);
}

module camera() {
    translate([-70, 15.5, 3]) cylinder(h = 15, r = 2.5);
    translate([-70, -15.5, 3]) cylinder(h = 15, r = 2.5);

    translate([-82, 0, 50]) cube ([10, 21, 3], center = true);
    translate([-82, 0, 30]) cube ([10, 21, 3], center = true);

    translate([-70, 0, 18]) cube ([19, 48, 3], center = true);
    translate([-78, 0, 40]) cube ([3, 48, 43], center = true);
    translate([-87, 0, 40]) cube ([1.5, 40, 28], center = true);
    
    translate([-89, 10, 40]) cube ([3, 9, 9], center = true);

}


module antenna() {
    cylinder(h = 112, r = 4.5);
    translate([0, 0, 112]) sphere(d = 9);
}

module car() {
    linear_extrude(3) base_plate();
    translate([-44, 28, -5]) rotate([0, 90, 90]) motor();
    translate([40, 28, -5]) rotate([0, 90, 90]) mirror([0, 1, 0]) motor();
    translate([-44, -28, -5]) rotate([0, 90, 90]) mirror([0, 0, 1])motor();
    translate([40, -28, -5]) rotate([0, 90, 270]) motor();
    battery();
    translate([5, 0, 0]) motor_shield();
    camera();
    translate([-20, 32, 0]) antenna();
}

translate([0,0, 16]) car();

