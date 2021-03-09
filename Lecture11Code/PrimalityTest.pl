#!/usr/bin/env perl

##  PrimalityTest.pl
##  Author: Avi Kak
##  Date:   February 28, 2016

##  An implementation of the Miller-Rabin primality test

### You can call this script with either no comamnd-line args or with just one
### command-line arg.  If you call it with no args, it returns primality results on a
### set of randomly altered 36 primes.  On the other hand, if you call it with just
### one arg, it returns the answer for that integer.

use strict;
use warnings;

unless (@ARGV) {
    my @primes = qw[ 179 233 283 353 419 467 547 607 661 739 811 877
                     947 1019 1087 1153 1229 1297 1381 1453 1523 1597
                     1663 1741 1823 1901 7001 7109 7211 7307 7417 7507
                     7573 7649 7727 7841 ];                                  #(M1)
    foreach my $p (@primes) {                                                #(M2)
        $p += 1 + int(rand(10));                                             #(M3)
        my $probability_of_prime = test_integer_for_prime($p);               #(M4)
        $probability_of_prime > 0 ?                                          #(M5)
          print "$p is prime with probability: $probability_of_prime\n" :    #(M6)
          print "$p is composite\n";                                         #(M7)         
    }
} elsif (@ARGV == 1) {                                                       #(M8)
    my $p = shift;                                                           #(M9)
    die "Your number is too large for this script. Instead, try the " .
        "script 'PrimalityTestWithBigInt.pl'\n"
        if $p > 0x7f_ff_ff_ff;                                               #(M10)
    my $probability_of_prime = test_integer_for_prime($p);                   #(M11)
    $probability_of_prime > 0 ?                                              
      print "$p is prime with probability: $probability_of_prime\n" :   
      print "$p is composite\n";                                             #(M12)          
} else {                                                                     #(M13)
    die "You cannot call 'PrimalityTest.py' with more " .             
        "than one command-line argument";                                    #(M14)
}

sub test_integer_for_prime {                                                 #(A1)
    my $p = shift;                                                           #(A2)
    return 0 if $p == 1;                                                     #(A3)
    my @probes = (2,3,5,7,11,13,17);                                         #(A4)
    my @in_probes = grep {$p == $_} @probes;                                 #(A5)
    return 1 if @in_probes;                                                  #(A6)
    my $p_mod_a = 1;                                                         #(A7)
    map { $p_mod_a = 0 if $p % $_ == 0 } @probes;                            #(A8)
    return 0 if $p_mod_a == 0;                                               #(A9)
    my ($k, $q) = (0, $p - 1);                                               #(A10)
    while (! ($q & 1)) {                                                     #(A11)
        $q >>= 1;                                                            #(A12)
        $k += 1;                                                             #(A13)
    }                                                         
    my ($a_raised_to_q, $a_raised_to_jq, $primeflag);                        #(A14)
    foreach my $a (@probes) {                                                #(A15)
        my ($base,$exponent) = ($a,$q);                                      #(A16)
        my $a_raised_to_q = 1;                                               #(A17)
        while ((int($exponent) > 0)) {                                       #(A18)
            $a_raised_to_q = ($a_raised_to_q * $base) % $p 
                                              if int($exponent) & 1;         #(A19)
            $exponent = $exponent >> 1;                                      #(A20)
            $base = ($base * $base) % $p;                                    #(A21)
        }
        next if $a_raised_to_q == 1;                                         #(A22)
        next if ($a_raised_to_q == ($p - 1)) && ($k > 0);                    #(A23)
        $a_raised_to_jq = $a_raised_to_q;                                    #(A24)
        $primeflag = 0;                                                      #(A25)
        foreach my $j (0 .. $k - 2) {                                        #(A26)
            $a_raised_to_jq = ($a_raised_to_jq ** 2) % $p;                   #(A27)
            if ($a_raised_to_jq == $p-1) {                                   #(A28)
                $primeflag = 1;                                              #(A29)
                last;                                                        #(A30)
            }
        }
        return 0 if ! $primeflag;                                            #(A31)
    }
    my $probability_of_prime = 1 - 1.0/(4 ** scalar(@probes));               #(A32)
    return $probability_of_prime;                                            #(A33)
}
