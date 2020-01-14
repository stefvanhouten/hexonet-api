#!/usr/bin/perl
use Net::EPP::Client;
 
my $epp = Net::EPP::Client->new(
        host    => 'testdrs.domain-REGISTRY.nl',
        port    => 700,
        ssl     => 1,
        frames  => 1,
);
 
my $greeting = $epp->connect;
$epp->send_frame('query.xml');
my $answer = $epp->get_frame;
my $filename = 'result.xml';

open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
print $fh $answer;
close $fh;