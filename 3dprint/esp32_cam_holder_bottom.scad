

difference() {
    cube([40, 14, 3], center = true);

    translate([13.5, 0, 0]) cylinder(h = 5, r = 2, $fn = 100, center=true);
    translate([-13.5, 0, 0]) cylinder(h = 5, r = 2, $fn = 100, center=true);

}


difference() {
    translate([0, 0, 6]) cylinder(h = 14, r = 7, $fn = 100, center=true);
    translate([0, -9, 11]) rotate([60, 0, 0]) cube([20, 14, 10], center = true);
    translate([0, 9, 11]) rotate([-60, 0, 0]) cube([20, 14, 10], center = true);
    translate([0, 0, 9.5]) rotate([0, 90,0])  cylinder(h = 16, r = 1.6, $fn = 100, center=true);
    translate([8, 0, 7]) cube([5, 10, 13], center = true);
    translate([-8, 0, 7]) cube([5, 10, 13], center = true);
}



translate([0, 20, 0]) rotate([180, 0, 0,]) { 
    difference() {
        cube([40, 14, 3], center = true);

        translate([12.5, 0, 0]) cylinder(h = 5, r = 2, $fn = 100, center=true);
        translate([-12.5, 0, 0]) cylinder(h = 5, r = 2, $fn = 100, center=true);
    }
    
    difference() {
        translate([7, 0, -7]) cube([3, 14, 12], center = true);
        translate([7, 0, -8.5]) rotate([0, 90,0]) cylinder(h = 5, r = 1.6, $fn = 100, center=true);
        translate([7, 7, -12]) rotate([50, 0, 0]) cube([5, 11, 6], center = true);
        translate([7, -7, -12]) rotate([-50, 0, 0]) cube([5, 11, 6], center = true);
    }
    
    difference() {
        translate([-7, 0, -7]) cube([3, 14, 12], center = true);
        translate([-7, 0, -8.5]) rotate([0, 90,0]) cylinder(h = 5, r = 1.6, $fn = 100, center=true);
        translate([-7, 7, -12]) rotate([50, 0, 0]) cube([5, 11, 6], center = true);
        translate([-7, -7, -12]) rotate([-50, 0, 0]) cube([5, 11, 6], center = true);
    }

}
