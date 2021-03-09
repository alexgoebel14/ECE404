#!/usr/bin/env perl

##  PrimalityTestWithBigInt.pl
##  Author: Avi Kak
##  Date: February 28, 2016 

use strict;
use warnings;
use Math::BigInt;    

die "\nUsage:   $0  <integer> \n" unless @ARGV == 1;                         #(M1)

my $p = shift @ARGV;                                                         #(M2)
$p = Math::BigInt->new( "$p" );                                              #(M3)

my $answer = test_integer_for_prime($p);                                     #(M4)
if ($answer) {                                                               #(M5)
    print "$p is prime with probability: $answer\n";                         #(M6)
} else {                                     
    print "$p is composite\n";                                               #(M7)
}

sub test_integer_for_prime {                                                 #(A1)
    my $p = shift;                                                           #(A2)
    return 0 if $p->is_one();                                                #(A3)
    my @probes = qw[ 2 3 5 7 11 13 17 ];                                     #(A4)
    foreach my $a (@probes) {                                                #(A5)
        $a = Math::BigInt->new("$a");                                        #(A6)
        return 1 if $p->bcmp($a) == 0;                                       #(A7)
        return 0 if $p->copy()->bmod($a)->is_zero();                         #(A8)
    }
    my ($k, $q) = (0, $p->copy()->bdec());                                   #(A9)
    while (! $q->copy()->band( Math::BigInt->new("1"))) {                    #(A10)
        $q->brsft( 1 );                                                      #(A11)
        $k += 1;                                                             #(A12)
    }
    my ($a_raised_to_q, $a_raised_to_jq, $primeflag);                        #(A13)
    foreach my $a (@probes) {                                                #(A14)
        my $abig = Math::BigInt->new("$a");                                  #(A15)
        my $a_raised_to_q = $abig->bmodpow($q, $p);                          #(A16)
        next if $a_raised_to_q->is_one();                                    #(A17)
        my $pdec = $p->copy()->bdec();                                       #(A18)
        next if ($a_raised_to_q->bcmp($pdec) == 0) && ($k > 0);              #(A19)
        $a_raised_to_jq = $a_raised_to_q;                                    #(A20)
        $primeflag = 0;                                                      #(A21)
        foreach my $j (0 .. $k - 2) {                                        #(A22)
            my $two = Math::BigInt->new("2");                                #(A23)
            $a_raised_to_jq = $a_raised_to_jq->copy()->bmodpow($two, $p);    #(A24)
            if ($a_raised_to_jq->bcmp( $p->copy()->bdec() ) == 0 ) {         #(A25)
                $primeflag = 1;                                              #(A26)
                last;                                                        #(A27)
            }
        }
        return 0 if ! $primeflag;                                            #(A28)
    }
    my $probability_of_prime = 1 - 1.0/(4 ** scalar(@probes));               #(A29)
    return $probability_of_prime;                                            #(A30)
}
