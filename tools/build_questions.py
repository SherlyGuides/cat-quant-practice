"""Builds questions.json from the question bank below and checks every answer.

Each question carries `check`: a computed value that must equal the text of the
option marked correct. Run:  python3 tools/build_questions.py
"""
import json
import math
from fractions import Fraction
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def q(qid, topic, level, text, options, answer, solution, explanation, check):
    return dict(id=qid, topic=topic, level=level, text=text, options=options,
                answer=answer, solution=solution, explanation=explanation, check=check)


# ---------- independent computations used to verify each key ----------
def power_in_factorial(n, p):
    k, e = 0, p
    while e <= n:
        k += n // e
        e *= p
    return k


def factorise(n):
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


C = {}
C['b1q1'] = pow(7, 103, 25)
C['b1q2'] = min(power_in_factorial(50, 2) // 2, power_in_factorial(50, 3))
C['b1q3'] = sum(1 for d in range(1, 2161) if 2160 % d == 0 and math.isqrt(d) ** 2 == d)
C['b1q4'] = len({tuple(sorted((a, 720 * 12 // a))) for a in range(12, 721, 12)
                 if 720 % a == 0 and math.gcd(a, 720 * 12 // a) == 12 and math.lcm(a, 720 * 12 // a) == 720})
# AP with S20 = 610, S30 = 1365
d_ap = Fraction(91 - 61, 10); a_ap = (61 - 19 * d_ap) / 2
assert 10 * (2 * a_ap + 19 * d_ap) == 610 and 15 * (2 * a_ap + 29 * d_ap) == 1365
C['b1q5'] = int(a_ap + 39 * d_ap)

C['b2q1'] = 49 * 6 + 52 * 6 - 50 * 11
C['b2q2'] = 31 * 15 - 30 * 14
milk_frac = Fraction(32, 40); C['b2q3'] = int(60 / milk_frac - 60)
C['b2q4'] = float(80 * Fraction(9, 10) ** 3)
fa, fb, ft = Fraction(2, 5), Fraction(7, 10), Fraction(3, 5)
r = (fb - ft) / (ft - fa); C['b2q5'] = f'{r.numerator}:{r.denominator}'

C['b3q1'] = round((1.25 * 0.80 - 1) * 100, 6)
C['b3q2'] = round((1.40 * 0.9 * 0.9 - 1) * 100, 2)
C['b3q3'] = int(150 / Fraction(10, 100) ** 2)
done = 4 * (Fraction(1, 12) + Fraction(1, 18)); C['b3q4'] = int((1 - done) * 18)
rel_ms = Fraction(240, 16); C['b3q5'] = int(rel_ms * Fraction(18, 5) + 6)

C['b4q1'] = (20 + 21 - math.isqrt(20 ** 2 + 21 ** 2)) // 2
C['b4q2'] = math.isqrt(17 ** 2 - 8 ** 2) + math.isqrt(17 ** 2 - 15 ** 2)
C['b4q3'] = int(Fraction(1, 3) * 36 * 8 / (Fraction(4, 3) * 8))
n_poly = 360 // (180 - 156); C['b4q4'] = n_poly * (n_poly - 3) // 2
C['b4q5'] = abs(0 * (6 - 6) + 6 * (6 - 0) + (-6) * (0 - 6)) // 2

roots = [x for x in range(-20, 21) if x * x - 7 * x + 10 == 0]; C['b5q1'] = sum(x ** 3 for x in roots)
C['b5q2'] = sum(1 for x in range(-50, 51) if abs(x - 3) + abs(x + 2) <= 9)
C['b5q3'] = [x for x in range(2, 50) if (x - 1) * (x + 1) == 8][0]
f = lambda x: 2 * x + 3; g = lambda x: x * x - 1; C['b5q4'] = f(g(2)) - g(f(1))
C['b5q5'] = int(max(min(Fraction(x, 100) + 5, 11 - 2 * Fraction(x, 100)) for x in range(-1000, 1001)))

C['b6q1'] = len(set(permutations('LETTER')))
seats = [p for p in permutations(range(5))]  # fix person 0 at a seat; arrange 1..5
C['b6q2'] = sum(1 for p in seats if abs(([0] + [x + 1 for x in p]).index(1) - ([0] + [x + 1 for x in p]).index(2)) not in (1, 5))
def is_prime(n): return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))
pr = Fraction(sum(1 for a in range(1, 7) for b in range(1, 7) if is_prime(a + b)), 36); C['b6q3'] = f'{pr.numerator}/{pr.denominator}'
C['b6q4'] = sum(1 for a in range(1, 11) for b in range(1, 11) if 10 - a - b >= 1)
C['b6q5'] = 35 + 30 - (60 - 12)

BLOCKS = [
 dict(id='b1', name='Numbers', blurb='Remainders, factorials, factors, HCF & LCM, progressions', qs=[
  q('b1q1', 'Remainders', 'Medium', 'What is the remainder when 7<sup>103</sup> is divided by 25?',
    ['7', '18', '2', '24'], 1,
    ['7<sup>2</sup> = 49 = 50 − 1, so 7<sup>2</sup> leaves remainder −1 when divided by 25.',
     'Then 7<sup>4</sup> = (7<sup>2</sup>)<sup>2</sup> leaves remainder (−1)<sup>2</sup> = 1.',
     '103 = 4 × 25 + 3, so 7<sup>103</sup> = (7<sup>4</sup>)<sup>25</sup> × 7<sup>3</sup> leaves remainder 1<sup>25</sup> × 7<sup>3</sup> = 343.',
     '343 = 13 × 25 + 18, so the remainder is <b>18</b>.'],
    'Look for a small power of the base that is 1 or −1 more or less than a multiple of the divisor. Once you have it, the huge power collapses to a small one. '
    'Option 7 is the remainder of 7<sup>1</sup>; 24 is what you get if you stop at 7<sup>2</sup> ≡ −1 and forget the leftover 7<sup>3</sup>.',
    C['b1q1']),
  q('b1q2', 'Factorials', 'Medium', 'What is the highest power of 12 that divides 50! exactly?',
    ['22', '23', '47', '16'], 0,
    ['12 = 2<sup>2</sup> × 3, so count the 2s and the 3s in 50!.',
     'Power of 2 in 50! = ⌊50/2⌋ + ⌊50/4⌋ + ⌊50/8⌋ + ⌊50/16⌋ + ⌊50/32⌋ = 25 + 12 + 6 + 3 + 1 = 47.',
     'Each 12 needs two 2s, so the 2s allow ⌊47/2⌋ = 23 twelves.',
     'Power of 3 in 50! = ⌊50/3⌋ + ⌊50/9⌋ + ⌊50/27⌋ = 16 + 5 + 1 = 22.',
     'The scarcer resource decides: min(23, 22) = <b>22</b>.'],
    'For a composite divisor, split it into prime powers, count each prime in n! with the ⌊n/p⌋ + ⌊n/p²⌋ + … rule, divide by the exponent, and take the minimum. '
    '23 is the trap of checking only the 2s; 47 forgets that 12 needs two 2s; 16 counts only the multiples of 3 once.',
    C['b1q2']),
  q('b1q3', 'Factors', 'Easy', 'How many factors of 2160 are perfect squares?',
    ['4', '8', '6', '12'], 2,
    ['Factorise: 2160 = 2<sup>4</sup> × 3<sup>3</sup> × 5.',
     'A perfect-square factor needs an even power of every prime.',
     'Power of 2 can be 0, 2 or 4 (3 choices); power of 3 can be 0 or 2 (2 choices); power of 5 must be 0 (1 choice).',
     'Total = 3 × 2 × 1 = <b>6</b>: 1, 4, 9, 16, 36, 144.'],
    'Counting factors is always "choices for each exponent, multiplied". The square restriction just limits each exponent to even values. '
    '8 comes from allowing 5<sup>1</sup>; 12 is the number of factors of 2<sup>4</sup> × 3<sup>2</sup>, which forgets the evenness rule on the 2s.',
    C['b1q3']),
  q('b1q4', 'HCF & LCM', 'Hard', 'Two positive numbers have HCF 12 and LCM 720. How many such pairs of numbers exist (order does not matter)?',
    ['3', '4', '6', '8'], 1,
    ['Write the numbers as 12a and 12b with a and b co-prime.',
     'LCM = 12ab = 720, so ab = 60 = 2<sup>2</sup> × 3 × 5.',
     'Because a and b are co-prime, each prime power (4, 3, 5) must go wholly to a or wholly to b.',
     'Three prime powers can be split in 2<sup>3</sup> = 8 ordered ways, i.e. 8/2 = <b>4</b> unordered pairs: (1, 60), (4, 15), (3, 20), (5, 12).',
     'The number pairs are (12, 720), (48, 180), (36, 240), (60, 144).'],
    'With HCF h and LCM l, the problem reduces to splitting l/h into two co-prime parts: 2<sup>k−1</sup> unordered ways for k distinct primes. '
    'The common slip is splitting 60 into any two factors, e.g. (2, 30) or (6, 10), which are not co-prime and would change the HCF.',
    C['b1q4']),
  q('b1q5', 'Progressions', 'Medium', 'The sum of the first 20 terms of an arithmetic progression is 610 and the sum of the first 30 terms is 1365. What is its 40th term?',
    ['122', '116', '119', '120'], 2,
    ['S<sub>n</sub> = (n/2)(2a + (n − 1)d).',
     'S<sub>20</sub> = 10(2a + 19d) = 610, so 2a + 19d = 61.',
     'S<sub>30</sub> = 15(2a + 29d) = 1365, so 2a + 29d = 91.',
     'Subtract: 10d = 30, so d = 3 and 2a = 61 − 57 = 4, a = 2.',
     'T<sub>40</sub> = a + 39d = 2 + 117 = <b>119</b>.'],
    'Turning each sum into a "2a + (n − 1)d" equation gives two simple linear equations. '
    'Shortcut: S<sub>n</sub>/n is the average of the first n terms, which equals the term at position (n + 1)/2. So the 10.5th term is 30.5 and the 15.5th term is 45.5; '
    '5 positions add 15, so d = 3. 122 and 116 are the 41st and 39th terms.',
    C['b1q5']),
 ]),
 dict(id='b2', name='Averages & Mixtures', blurb='Averages, weighted averages, alligation, replacement', qs=[
  q('b2q1', 'Averages', 'Easy', 'The average of 11 results is 50. The average of the first six is 49 and the average of the last six is 52. What is the sixth result?',
    ['53', '56', '50', '58'], 1,
    ['Total of all 11 = 11 × 50 = 550.',
     'First six total = 6 × 49 = 294; last six total = 6 × 52 = 312.',
     'Adding the two groups counts the 6th result twice: 294 + 312 = 606.',
     'Sixth result = 606 − 550 = <b>56</b>.'],
    'Whenever two groups overlap in exactly one item, (group 1 total + group 2 total − overall total) isolates that item. '
    'Deviation method: the first six are 6 below average in total and the last six are 12 above, so the shared result is 50 − 6 + 12 = 56.',
    C['b2q1']),
  q('b2q2', 'Averages', 'Easy', 'The average age of 30 students is 14 years. When the teacher’s age is included, the average rises by 1 year. How old is the teacher?',
    ['44', '45', '46', '31'], 1,
    ['Students’ total = 30 × 14 = 420.',
     'With the teacher there are 31 people averaging 15: total = 465.',
     'Teacher = 465 − 420 = <b>45</b>.'],
    'Deviation shortcut: the teacher brings their own share of the new average (15) and also lifts each of the 30 students by 1. Teacher = 15 + 30 × 1 = 45. '
    '44 uses 14 + 30; 31 forgets the teacher’s own share.',
    C['b2q2']),
  q('b2q3', 'Alligation', 'Medium', 'Milk costs ₹40 per litre. How many litres of water must be added to 60 litres of milk so that the mixture is worth ₹32 per litre?',
    ['12', '15', '18', '20'], 1,
    ['Water costs nothing, so the value of the mixture is all from the milk: 60 × 40 = ₹2400.',
     'At ₹32 per litre, ₹2400 buys 2400 ÷ 32 = 75 litres of mixture.',
     'Water added = 75 − 60 = <b>15</b> litres.'],
    'Alligation view: milk at 40 and water at 0 mix to 32, so milk : water = (32 − 0) : (40 − 32) = 4 : 1. 60 litres of milk needs 15 of water. '
    '12 comes from taking 20% of 60, but the price falls by 20% because water becomes 20% of the final mixture, not 20% of the milk.',
    C['b2q3']),
  q('b2q4', 'Replacement', 'Medium', 'A vessel holds 80 litres of pure milk. 8 litres are taken out and replaced with water, and this is done three times in all. How much milk is left?',
    ['56 litres', '57.6 litres', '58.32 litres', '64.8 litres'], 2,
    ['Each replacement removes 8/80 = 1/10 of whatever milk is in the vessel, leaving 9/10 of it.',
     'After three rounds: 80 × (9/10)<sup>3</sup> = 80 × 0.729 = <b>58.32</b> litres.'],
    'Repeated replacement is compound decay: final = initial × (1 − removed/capacity)<sup>n</sup>. '
    '56 litres assumes 8 litres of milk leaves every time (simple subtraction), which is wrong after the first round because later you remove a mixture. 64.8 litres is the answer after two rounds.',
    C['b2q4']),
  q('b2q5', 'Alligation', 'Hard', 'Alloy A has gold and copper in the ratio 2 : 3, and alloy B has them in the ratio 7 : 3. In what ratio must A and B be melted together to get an alloy with gold and copper in the ratio 3 : 2?',
    ['2:1', '1:2', '1:3', '3:2'], 1,
    ['Work with the fraction of gold: A is 2/5 = 0.4, B is 7/10 = 0.7, and the target is 3/5 = 0.6.',
     'Alligation: A : B = (0.7 − 0.6) : (0.6 − 0.4) = 0.1 : 0.2 = <b>1 : 2</b>.',
     'Check: 1 kg of A and 2 kg of B give 0.4 + 1.4 = 1.8 kg of gold in 3 kg, i.e. 0.6.'],
    'Alligation only works on the same kind of quantity, here the gold fraction of each alloy. Converting both ratios to “share of gold” is the key step. '
    '2 : 1 is the classic slip of writing the differences the wrong way round: the alloy closer to the target needs the larger share.',
    C['b2q5']),
 ]),
 dict(id='b3', name='Arithmetic', blurb='Percentages, profit & loss, interest, time & work, speed', qs=[
  q('b3q1', 'Percentages', 'Easy', 'A earns 25% more than B, and B earns 20% less than C. How does A’s salary compare with C’s?',
    ['A earns 5% more', 'A earns 5% less', 'A and C earn the same', 'A earns 25% more'], 2,
    ['Let C = 100. B is 20% less: B = 80.',
     'A is 25% more than B: A = 80 × 1.25 = 100.',
     'So A = C: they earn <b>the same</b>.'],
    'A 20% fall is ×4/5 and a 25% rise is ×5/4; they cancel exactly. Remember the pair 20% ↔ 25%: a fall of 1/5 is undone by a rise of 1/4. '
    'The “5%” options come from adding and subtracting the percentages directly, which only works when they are applied to the same base.',
    C['b3q1']),
  q('b3q2', 'Profit & Loss', 'Medium', 'A trader marks goods 40% above cost and then allows two successive discounts of 10% each. What is the profit percentage?',
    ['20%', '12%', '13.4%', '14.6%'], 2,
    ['Let cost = 100. Marked price = 140.',
     'After the first 10% discount: 140 × 0.9 = 126.',
     'After the second: 126 × 0.9 = 113.4.',
     'Profit = 113.4 − 100 = <b>13.4%</b>.'],
    'Successive changes multiply: 1.4 × 0.9 × 0.9 = 1.134. Two 10% discounts are a single 19% discount (10 + 10 − 10×10/100), not 20%. '
    '20% subtracts the discounts from the markup; 12% treats the two discounts as 20% off and still subtracts wrongly.',
    C['b3q2']),
  q('b3q3', 'Interest', 'Easy', 'The difference between the compound interest and the simple interest on a sum for 2 years at 10% per annum is ₹150. What is the sum?',
    ['₹7,500', '₹15,000', '₹1,500', '₹30,000'], 1,
    ['For 2 years, CI − SI = P × (r/100)<sup>2</sup>: it is the interest earned on the first year’s interest.',
     '150 = P × (0.1)<sup>2</sup> = P × 0.01.',
     'P = <b>₹15,000</b>.'],
    'The only extra money under compound interest in year 2 is interest on year 1’s interest: P × r/100 × r/100. '
    'For 3 years the gap is P(r/100)<sup>2</sup>(3 + r/100). ₹1,500 multiplies by 10 instead of 100.',
    C['b3q3']),
  q('b3q4', 'Time & Work', 'Medium', 'A can finish a job in 12 days and B in 18 days. They work together for 4 days, and then A leaves. How many more days does B need to finish the job?',
    ['6', '7', '8', '10'], 2,
    ['Take the job as 36 units (LCM of 12 and 18). A does 3 units a day, B does 2.',
     'Together for 4 days: (3 + 2) × 4 = 20 units.',
     'Remaining = 36 − 20 = 16 units, which B does at 2 a day: <b>8</b> more days.'],
    'Choosing total work as the LCM of the individual times makes every rate a whole number and avoids fractions. '
    '6 days assumes B works at A’s rate; 10 days forgets that B also worked during the first 4 days.',
    C['b3q4']),
  q('b3q5', 'Speed, Time & Distance', 'Medium', 'A train 240 m long passes a man walking at 6 km/h in the same direction in 16 seconds. What is the speed of the train?',
    ['54 km/h', '60 km/h', '48 km/h', '66 km/h'], 1,
    ['To pass the man, the train covers its own length, 240 m, at the relative speed.',
     'Relative speed = 240 ÷ 16 = 15 m/s = 15 × 18/5 = 54 km/h.',
     'Same direction, so relative speed = train − man: train = 54 + 6 = <b>60 km/h</b>.'],
    'Relative speed subtracts for same direction and adds for opposite directions. '
    '54 km/h stops at the relative speed; 48 km/h subtracts the man’s speed instead of adding it back (that would be right only if they were moving towards each other); 66 km/h adds the man’s speed twice. Draw the directions before choosing + or −.',
    C['b3q5']),
 ]),
 dict(id='b4', name='Geometry', blurb='Triangles, circles, polygons, mensuration, coordinates', qs=[
  q('b4q1', 'Triangles', 'Easy', 'A right triangle has legs of 20 cm and 21 cm. What is the radius of its inscribed circle?',
    ['5 cm', '6 cm', '10 cm', '14.5 cm'], 1,
    ['Hypotenuse = √(20² + 21²) = √841 = 29 cm.',
     'For a right triangle, inradius r = (a + b − c)/2 = (20 + 21 − 29)/2 = <b>6 cm</b>.',
     'Check with r = Area/s: area = 210, semi-perimeter s = 35, r = 6.'],
    '20-21-29 is a Pythagorean triplet worth remembering. The formula r = (a + b − c)/2 comes from the two tangents from each acute vertex. '
    '14.5 cm is the circumradius (half the hypotenuse), the most common mix-up with the inradius.',
    C['b4q1']),
  q('b4q2', 'Circles', 'Medium', 'Two parallel chords of a circle of radius 17 cm have lengths 16 cm and 30 cm, and lie on opposite sides of the centre. How far apart are the chords?',
    ['7 cm', '17 cm', '23 cm', '25 cm'], 2,
    ['The perpendicular from the centre bisects a chord, so distance = √(r² − (half-chord)²).',
     '16 cm chord: √(17² − 8²) = √225 = 15 cm from the centre.',
     '30 cm chord: √(17² − 15²) = √64 = 8 cm from the centre.',
     'Opposite sides of the centre, so the distances add: 15 + 8 = <b>23 cm</b>.'],
    '8-15-17 is a triplet, which makes both distances whole numbers. If the chords were on the same side, the answer would be 15 − 8 = 7 cm, which is the trap option.',
    C['b4q2']),
  q('b4q3', 'Mensuration', 'Medium', 'A solid cone of base radius 6 cm and height 8 cm is melted and recast into solid spheres of radius 2 cm. How many spheres are made?',
    ['6', '9', '18', '27'], 1,
    ['Cone volume = (1/3)πr²h = (1/3)π × 36 × 8 = 96π cm³.',
     'Sphere volume = (4/3)πr³ = (4/3)π × 8 = (32/3)π cm³.',
     'Number of spheres = 96π ÷ (32π/3) = 96 × 3/32 = <b>9</b>.'],
    'Melting and recasting keeps volume the same. Write both volumes with π and cancel it. '
    '27 forgets the 1/3 in the cone’s volume; 18 uses r² instead of r³ for the sphere.',
    C['b4q3']),
  q('b4q4', 'Polygons', 'Easy', 'Each interior angle of a regular polygon is 156°. How many diagonals does it have?',
    ['75', '90', '105', '120'], 1,
    ['Exterior angle = 180° − 156° = 24°.',
     'Exterior angles of any polygon add to 360°, so n = 360 ÷ 24 = 15 sides.',
     'Diagonals = n(n − 3)/2 = 15 × 12/2 = <b>90</b>.'],
    'Always go through the exterior angle: it gives the number of sides in one division. '
    '105 is ¹⁵C₂, which counts the sides as well as the diagonals.',
    C['b4q4']),
  q('b4q5', 'Coordinate Geometry', 'Easy', 'What is the area of the triangle formed by the lines y = x, y = −x and y = 6?',
    ['18', '24', '36', '72'], 2,
    ['y = x and y = −x meet at the origin.',
     'y = 6 meets them at (6, 6) and (−6, 6).',
     'Base = distance between (−6, 6) and (6, 6) = 12; height = 6 (distance of the base from the origin).',
     'Area = ½ × 12 × 6 = <b>36</b> square units.'],
    'Find the vertices first; with a horizontal base, area is just ½ × base × height. '
    '18 uses a base of 6 (one side only); 72 forgets the ½.',
    C['b4q5']),
 ]),
 dict(id='b5', name='Algebra', blurb='Quadratics, inequalities, logarithms, functions', qs=[
  q('b5q1', 'Quadratic Equations', 'Medium', 'If α and β are the roots of x² − 7x + 10 = 0, what is α³ + β³?',
    ['133', '203', '313', '343'], 0,
    ['Sum of roots α + β = 7; product αβ = 10.',
     'α³ + β³ = (α + β)³ − 3αβ(α + β) = 343 − 3 × 10 × 7 = 343 − 210 = <b>133</b>.',
     'Check: the roots are 2 and 5, and 8 + 125 = 133.'],
    'Express symmetric expressions through the sum and product of roots; you never need the roots themselves. '
    '343 is just (α + β)³; 313 subtracts 3αβ but forgets the (α + β) factor; 203 is (α + β)(α² + β²), which misses the −αβ term in α² − αβ + β².',
    C['b5q1']),
  q('b5q2', 'Inequalities', 'Hard', 'How many integers x satisfy |x − 3| + |x + 2| ≤ 9?',
    ['6', '9', '10', '11'], 2,
    ['|x − 3| + |x + 2| is the total distance from x to 3 and to −2 on the number line.',
     'For any x between −2 and 3 that total is exactly 5, which is ≤ 9: all of −2…3 work.',
     'For x > 3: (x − 3) + (x + 2) = 2x − 1 ≤ 9 gives x ≤ 5.',
     'For x < −2: (3 − x) + (−2 − x) = 1 − 2x ≤ 9 gives x ≥ −4.',
     'So −4 ≤ x ≤ 5: <b>10</b> integers.'],
    'Read |x − a| as distance. Between the two points the sum is constant (the gap, 5); outside, it grows by 2 for every unit you move away. '
    'With 9 − 5 = 4 to spare, you can move 2 units beyond each end. 6 counts only −2…3; 9 or 11 are off-by-one slips at the endpoints.',
    C['b5q2']),
  q('b5q3', 'Logarithms', 'Easy', 'Solve log₂(x − 1) + log₂(x + 1) = 3.',
    ['x = −3', 'x = 2', 'x = 3', 'x = 9'], 2,
    ['Combine: log₂[(x − 1)(x + 1)] = 3, so x² − 1 = 2³ = 8.',
     'x² = 9, so x = 3 or x = −3.',
     'Logs need positive arguments: x − 1 > 0, so x > 1. Reject −3.',
     'Answer: <b>x = 3</b>.'],
    'After solving any log equation, check that every original log argument is positive. '
    'x = −3 is the classic extraneous root; x = 9 comes from treating log₂ 8 as 9 instead of 3.',
    C['b5q3']),
  q('b5q4', 'Functions', 'Easy', 'If f(x) = 2x + 3 and g(x) = x² − 1, what is f(g(2)) − g(f(1))?',
    ['−15', '−13', '0', '15'], 0,
    ['g(2) = 4 − 1 = 3, so f(g(2)) = f(3) = 9.',
     'f(1) = 5, so g(f(1)) = g(5) = 24.',
     'f(g(2)) − g(f(1)) = 9 − 24 = <b>−15</b>.'],
    'Evaluate composite functions from the inside out. f(g(x)) and g(f(x)) are generally different. '
    '15 has the subtraction reversed; 0 assumes the composition order does not matter.',
    C['b5q4']),
  q('b5q5', 'Functions', 'Medium', 'What is the maximum value of f(x) = min(x + 5, 11 − 2x) over all real x?',
    ['5', '7', '9', '11'], 1,
    ['x + 5 increases and 11 − 2x decreases, so their minimum is largest where the two are equal.',
     'x + 5 = 11 − 2x gives 3x = 6, x = 2.',
     'f(2) = 2 + 5 = <b>7</b>.'],
    'The maximum of the minimum of a rising and a falling line is at their intersection: anywhere else, one of them is lower. '
    '11 and 5 are each line’s value at x = 0, and 9 is a midpoint guess.',
    C['b5q5']),
 ]),
 dict(id='b6', name='Counting', blurb='Permutations, combinations, probability, sets', qs=[
  q('b6q1', 'Permutations', 'Easy', 'In how many different ways can the letters of the word LETTER be arranged?',
    ['90', '180', '360', '720'], 1,
    ['LETTER has 6 letters: L, E, T, T, E, R. E and T each appear twice.',
     'Arrangements = 6!/(2! × 2!) = 720/4 = <b>180</b>.'],
    'Divide by the factorial of each repeat count, because swapping identical letters gives the same word. '
    '720 ignores the repeats; 360 divides out only one of the two pairs.',
    C['b6q1']),
  q('b6q2', 'Circular Arrangements', 'Medium', 'Six people sit around a round table. In how many ways can they sit if two particular people must not sit next to each other?',
    ['48', '72', '96', '120'], 1,
    ['Total circular arrangements of 6 = (6 − 1)! = 120.',
     'Arrangements with the two together: treat them as one unit, so 5 units around the table = 4! = 24, times 2 for their internal order = 48.',
     'Not together = 120 − 48 = <b>72</b>.'],
    'For “not together”, count all and subtract “together”. Circular arrangements fix one seat, which is why it is (n − 1)!. '
    '48 is the together count; 120 is the total.',
    C['b6q2']),
  q('b6q3', 'Probability', 'Medium', 'Two fair dice are thrown. What is the probability that the sum is a prime number?',
    ['1/3', '7/18', '5/12', '1/2'], 2,
    ['Possible prime sums: 2, 3, 5, 7, 11.',
     'Ways: 2 → 1, 3 → 2, 5 → 4, 7 → 6, 11 → 2. Total 15 of 36 outcomes.',
     'Probability = 15/36 = <b>5/12</b>.'],
    'For two dice, the number of ways to get sum s is 6 − |s − 7|. 7/18 (14/36) usually misses one way for 5 or 11; 1/2 is a guess.',
    C['b6q3']),
  q('b6q4', 'Distributions', 'Medium', 'How many solutions in positive integers does a + b + c = 10 have?',
    ['36', '45', '55', '66'], 0,
    ['Positive integers: give each of a, b, c one unit first, leaving 7 to distribute freely.',
     'Non-negative solutions of x + y + z = 7 = ⁹C₂ = 36 (7 stars and 2 bars).',
     'Equivalently, ⁽ⁿ⁻¹⁾C₍ᵣ₋₁₎ = ⁹C₂ = <b>36</b>.'],
    'Positive solutions of x₁ + … + x<sub>r</sub> = n number ⁿ⁻¹C<sub>r−1</sub>; non-negative ones number ⁿ⁺ʳ⁻¹C<sub>r−1</sub>. '
    '66 = ¹²C₂ counts non-negative solutions (zeros allowed), which the question excludes.',
    C['b6q4']),
  q('b6q5', 'Set Theory', 'Easy', 'In a group of 60 people, 35 like tea, 30 like coffee and 12 like neither. How many like both?',
    ['5', '13', '17', '23'], 2,
    ['People who like at least one = 60 − 12 = 48.',
     'n(T ∪ C) = n(T) + n(C) − n(T ∩ C): 48 = 35 + 30 − both.',
     'Both = 65 − 48 = <b>17</b>.'],
    'Always remove the “neither” group before using the union formula. 5 forgets the 12 who like neither (65 − 60).',
    C['b6q5']),
 ]),
]

# ---------- verify every key against its computed value ----------
def norm(v):
    s = str(v).replace('₹', '').replace(',', '').replace(' litres', '').replace(' cm', '').replace(' km/h', '').replace('%', '').replace('x = ', '').strip()
    try:
        return float(Fraction(s)) if '/' in s or s.replace('.', '').replace('−', '-').lstrip('-').isdigit() else s.replace('−', '-')
    except Exception:
        return s.replace('−', '-')

errors = []
for b in BLOCKS:
    for item in b['qs']:
        key = item['options'][item['answer']]
        chk = item['check']
        if item['id'] == 'b3q1':
            ok = chk == 0 and key == 'A and C earn the same'
        else:
            nk = norm(key.replace('−', '-'))
            nc = norm(chk)
            ok = (abs(float(nk) - float(nc)) < 1e-9) if isinstance(nk, float) and isinstance(nc, float) else str(nk) == str(nc)
        others = [norm(o.replace('−', '-')) for i, o in enumerate(item['options']) if i != item['answer']]
        dup = isinstance(norm(key), float) and any(isinstance(o, float) and abs(o - norm(key)) < 1e-9 for o in others)
        if not ok or dup or len(set(item['options'])) != 4:
            errors.append((item['id'], key, chk, 'duplicate option' if dup else ''))
if errors:
    raise SystemExit(f'Answer check failed: {errors}')

out = {'title': 'CAT Quant Practice', 'blocks': [{k: v for k, v in b.items() if k != 'qs'} | {'questions': [{k: v for k, v in it.items() if k != 'check'} for it in b['qs']]} for b in BLOCKS]}
(ROOT / 'questions.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
n = sum(len(b['qs']) for b in BLOCKS)
print(f'OK: {n} questions in {len(BLOCKS)} blocks, every key matches its computed answer.')
print('answer positions:', [it['answer'] for b in BLOCKS for it in b['qs']])
