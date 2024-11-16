difference() {
    cube([56, 33, 13], center=true); 
    translate([0, 0, 2]) cube([52, 29, 14], center=true);
    translate([26, 0, 3]) cube([5, 10, 8], center=true);
    translate([-26, 0, 3]) cube([5, 10, 8], center=true);
}

translate([23.5, 12.5, -2]) cube([5, 4.5, 8], true);
translate([-23.5, 12.5, -2]) cube([5, 4.5, 8], true);
translate([23.5, -12.5, -2]) cube([5, 4.5, 8], true);
translate([-23.5, -12.5, -2]) cube([5, 4.5, 8], true);

translate([23, 11.5, 3]) cylinder(h = 3, r = 1, $fn = 100, center=true);
translate([-23, 11.5, 3]) cylinder(h = 3, r = 1, $fn = 100, center=true);
translate([23, -11.5, 3]) cylinder(h = 3, r = 1, $fn = 100, center=true);
translate([-23, -11.5, 3]) cylinder(h = 3, r = 1, $fn = 100, center=true);