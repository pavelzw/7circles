### Introduction

Today, we will take a look at the so-called "Seven circles theorem".

While the statement of the theorem can be expressed in simple geometric terms,
the method we will use to prove it delves into seemingly unrelated concepts from hyperbolic geometry.

It involves a surprising change of perspective between Euclidean and hyperbolic space. On the way we will learn about
two different models of hyperbolic space, how distances are measured as well as circles and polygons in this hyperbolic setting. 
Mind you, this is not the only way to prove our theorem. The first proofs of the seven circles theorem in the 1970s did not wander through the lands of hyperbolic geometry but used mainly euclidean methods.

Let us now finally take a look at the seven circles theorem.

### Theorem statement

Let C be a circle containing six smaller circles, such that each inner circle is tangent to the outer circle and any two adjacent inner circles are also tangent to each other.

Let us also draw the hexagon formed by the intersection points of each inner circle with the outer circle.

The Seven-circles theorem then states that the three main diagonals of the hexagon will always meet at a single point.

Our goal is to now prove this statement.

We will be able to do this by embedding the problem into a hyperbolic framework.

First, we give a small introduction to hyperbolic geometry to then rephrase the problem in this setting with our newly
gained knowledge.

### Parallel axiom

Axiomatically, hyperbolic space differs from Euclidean space in that the parallel axiom does not hold.

The parallel axiom states that for every straight line g and every point P that does not lie on g, there is exactly one
straight line h that runs through P and is parallel to g.

By "parallel" we only mean that they do not intersect.

This property does not hold in hyperbolic space. Here, for every line g and point P there are several - even infinitely many - straight lines through P which are parallel to g, meaning they do not intersect g.

However, our representation here is misleading. Of course, g will be intersected by all but the original line h if we
follow them long enough.
<!-- [follow camera down right until intersection point] -->

Generally, we have the problem that we want to represent hyperbolic space in the Euclidean plane, namely this video.

So the question we are addressing now is:

How can we represent the hyperbolic in the Euclidean plane?

### Hyperbolic models

There are different models for the hyperbolic plane.

Such models simply map the hyperbolic to the Euclidean plane.

We take a closer look at the Poincaré and Klein models.

There are however multiple other models, which can be helpful in other contexts.

## Poincaré model i

First, let's take a closer look at the Poincaré model.

The representation of the hyperbolic plane in the Poincaré model is limited to the unit disk.

The geodesics of the Poincaré model are - unlike straight lines in Euclidean space - 
circle segments that intersect the unit circle at a right angle.
<!-- Draw right angles -->

This illustrates why the parallel axiom does not apply here:

For a point P and a geodesic g, we can find arbitrarily many other geodesics that intersect P but not g.

### Poincaré model ii

Even if it appears that way at first glance, the hyperbolic plane is by no means limited.

If we let a point move in one direction with constant speed, we notice that it never reaches the boundary of the
Poincaré model.

The unit circle itself does not belong to the Poincaré model and can not be reached.



This distortion can be visualized by looking at a tiling of the hyperbolic plane.

All these triangles have the same hyperbolic shape and area.

The Poincaré model thus provides a highly distorted representation of hyperbolic space.

## Klein model

Now, let us consider the Klein model.

We will see strong similarities to the Poincaré model.

The biggest difference is that geodesics here actually correspond to Euclidean lines.

As in the Poincaré model, we are limited by the unit circle.  
Thus, the parallel axiom does not apply here either.



The Klein model also gives a very distorted represenation of hyperbolic space.

Here, we see the same tiling as before, now in the Klein model.

Distances become larger and larger towards the border, making the triangles seem smaller, the closer we get to it.

## Model transformations

Since both models represent the same space, it is natural that there are mappings that identify the points of the models
with each other.

We call them f and f^-1.

As we see here, the formulas for these maps are fairly simple.

With f and f^-1, we can now transfer objects from one model to the other, specifically geodesics.

Since the maps act pointwise, intersections between geodesics are preserved.

<!-- todo add intersections between the two geodesics -->

## Rephrased theorem

This helps us rephrase the Seven-Circles-Theorem:

Let C be a circle containing six smaller circles, such that each inner circle is tangent to the outer circle and any two
adjacent inner circles are also tangent to each other.

Drawing the hyperbolic hexagon formed by the intersection points of each inner circle with the outer circle, the three
main diagonals will always meet at a single point.

After having proven this new statement, we simply apply the transformation from the Poincaré to the Klein model and have
thus also proven the original theorem.

### Hyperbolic circles

Now we introduce some new concepts in hyperbolic space.

Let's take a closer look at the behavior of circles and their radii in this setting.

To do this, we compare it to Euclidean circles we are familiar with.

A circle consists of all points that are the same distance from their center P.

In Euclidean space, we measure distance with the Euclidean distance function.

Hyperbolic disks, which we embed in the Poincaré model, are defined exactly like Euclidean circles. Except here, we use
a different distance function to measure lengths.

At the center of the Poincaré disk, the hyperbolic circles look the same as the Euclidean ones.

If we now change the center, the shape of the hyperbolic circles still corresponds to that of the Euclidean circles, but the
center of the Euclidean circles no longer corresponds to that of the hyperbolic ones.

## Hyperbolic radius

Let's take a closer look at the hyperbolic radius.

It is defined using the hyperbolic distance function, which measures the distance between two points b and c in the
hyperbolic plane.

For the calculation, we need the intersection points of the geodesic with the border of the unit disk.

We call these points a and d.

To evaluate the hyperbolic distance function, we interpret points a through d as numbers in the complex plane.

It might not look like it, but the hyperbolic circle has the same distance to its center at every point.

If we move the hyperbolic center to the border and look at the associated concentric circles, the hyperbolic radius
converges to infinity and we get so-called horodisks.

After obtaining an intuition for circles in hyperbolic space, we now want to also understand hyperbolic hexagons. From
there on, we will be able to define the alternating perimeter, which is of great importance to our main theorem.

### Hyperbolic polygons

A hyperbolic polygon is defined as in Euclidean space.

However, we will represent the curves connecting the vertices as circle segments, as always in the Poincaré model.

The corners of the polygon can be anywhere in the hyperbolic plane.

If the vertices all lie on the border of the Poincaré disk, we call our polygon ideal.

As in the Euclidean case, the perimeter of a hyperbolic polygon can be defined as the sum of the sidelengths.

Note that we are measuring the hyperbolic distance between the vertices.

In the case of hexagons, an even number of corners can be used to define an alternating perimeter.

Instead of taking the sum of all sidelengths, we now calculate the alternating sum, i.e., subtract every other length.

## Alternating perimeter i

So now let's look at the alternating perimeter of an ideal hexagon.

The problem here is that the individual segments S_k have infinite length since they touch the border.

Therefore, we cannot calculate the alternating perimeter directly.

However, geodesic segments that do not touch the boundary have finite length.

We will take advantage of this.

We define the alternating perimeter of an ideal hexagon using that of a non-ideal hexagon.

Since its edges have finite length, we can explicitly calculate the alternating perimeter here.

## Alternating perimeter ii

To do this, consider a sequence P_n of hyperbolic non-ideal hexagons that converge to an ideal hexagon P_∞.

We now put a disk at each vertex of P_n so that consecutive disks do not overlap.

Further we define S_k^~ as the length of the edge between the borders of the disks.

Obviously, these S_k^~ are finite.

If we change the radius of a disk, we add and subtract the same amount from the alternating perimeter. In this case S_1^~ and S_6^~ are changed.

Therefore, the alternating perimeter is independent of the size of our disks, in particular when our disks have radius zero.

Thus, the alternating sum of S_k is equal to the alternating sum of S_k^~.

If we let n go towards infinity, this equality still holds.

But since the lengths S_k^~ are now finite, we have actually found a meaningful calculation for the alternating perimeter.

### Main result (T_P)

Now let's consider an ideal hexagon.

If we connect the opposite sides of this hexagon, a triangle appears in the middle.

Let's call this triangle T_P.

We now prove the following equality:

For any ideal hexagon, the absolute value of the alternating perimeter is exactly twice the perimeter of T_P.

For the proof we first define the notion of a semi-ideal triangle.

It has two corners on the boundary of the circle - i.e., ideal points - and one corner in the hyperbolic plane.

In our ideal hexagon there are three such triangles: Y_1, Y_2 and Y_3.

Three other semi-ideal triangles which intersect the inner triangle T_P can be found opposite to the Y_k triangles.

We call them G_1, G_2 and G_3.

For hyperbolic triangles we define a notion similar to the alternating perimeter.

If we add disjoint horodisks at the two ideal vertices of the triangle, we get lengths L_1', L_2' and L_3'.

We use this to define the alternating perimeter of a semi-ideal triangle by adding the two blue lengths and subtracting
the red one.

The alternating perimeter does not depend on the size of each circle, since the same length is both added and
subtracted.

The triangles G_k and Y_k each share exactly one vertex for k = 1, ..., 3.

In each case, there is an isometry I_k that maps opposite triangles onto each other.

We can construct these isometries as follows:

With the help of so-called Möbius transformations - isometries in the hyperbolic plane - we can map the intersection of
the two triangles to the origin.

The two diagonals that intersect the point are now both straight lines through the origin.

Therefore, we can simply perform a point reflection at the origin, transforming one triangle onto the other.

Of course, the whole thing works not only for the first pair of triangles, but for all three of them.

Since we have an isometry between the two triangles, their alternating perimeter is the same.

We can write these formulas explicitly for all three pairs of triangles and bring the perimeter of G_k to the other
side.

By adding everything together, we obtain the following formula.

But what does this sum actually represent?

Let's look at the sum in the picture.

If we subtract the alternating perimeter of the G_i, a part of the sum cancels out with the alternating perimeter of the
Y_i.

We notice that we obtain twice the perimeter of the inner triangle as well as the alternating perimeter of the hexagon.

Overall, our equality follows.

### Final proof (epic)

Now we are finally ready to prove the Seven-Circles-Theorem.

Let's look at an ideal hyperbolic hexagon with circles tangent to the large circle such that adjacent circles touch at a
single point.

Taking a look at the alternating perimeter of this hexagon, we notice that the hexagon segments in the circles cancel
out. Therefore, the alternating perimeter is zero.

So the perimeter of the triangle in the middle is also zero, using the equality we just proved.

Thus, the main diagonals of the hexagon must meet at a single point.

All that's left is to perform the transformation from the Poincaré model back to the Klein model.

As mentioned before, the diagonals continue to run through a single point.

This corresponds exactly to the scenario from the original Seven Circles Theorem, which we have thus proved.
