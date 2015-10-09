#!/usr/local/bin/perl

use aan;
use strict;
use Getopt::Long;


my $metafile = '';
my $acl_file = '';
my $to_year = 2012;
my $release = 2012;
my $incites = 1;
my $outcites = 0;
my $nonself = 0;
my $help = 0;

GetOptions("release:i" => \$release,
		   "year:i" => \$to_year,
		   "incites" => \$incites,
		   "outcites" => \$outcites,
		   "nonself" => \$nonself,
		   "help" => \$help);


if($help)
{
		usage();
		exit;
}

$acl_file = "../$release/acl.txt";
$metafile = "../$release/acl-metadata.txt";


my %meta = aan::buildmeta($metafile);

my %incites = '';
my %outcites = '';

foreach my $paper_id (sort (keys(%meta))) {
	
	if(&aan::select_year($paper_id,$to_year) == 1) {
	my $auths = $meta{$paper_id};
    $auths =~ s/ ::: .+//;
    $auths =~ s/ :: /; /;
	my @fas = '';
    if ($auths ne "na")
	{
		if ($auths =~ m/;/) {
#@fas = split(/; /, $auths);
				@fas = @{aan::extract_authors($auths)};
		}
		else {
		    push(@fas, $auths);
		}
		foreach my $auth (@fas)
		{
				if($auth ne "") {
				$incites{$auth} = 0;
				$outcites{$auth} = 0;
				}
		}
	 }
	}
}





open (IN, $acl_file) || die ("Could not open network.\n");
chomp (my @network = <IN>);
close IN;


foreach my $pair (@network) {
	$pair =~ /(.+) ==> (.+)/;
	my ($from, $cites) = ($1, $2);

	if(&aan::select_year($from,$to_year) == 1 && &aan::select_year($cites,$to_year) == 1) {
	my $from_auths = $meta{$from};
	$from_auths =~ s/ ::: .+//;
	$from_auths =~ s/ :: /; /;
	my $cites_auths = $meta{$cites};
	$cites_auths =~ s/ ::: .+//;
	$cites_auths =~ s/ :: /; /;
	my (@fas, @cas);
	if (($from_auths ne "na") && ($cites_auths ne "na") && ($cites_auths ne "") && ($cites_auths ne "")) {
		if ($from_auths =~ m/;/) {
#@fas = split(/; /, $from_auths);
			@fas = @{aan::extract_authors($from_auths)};
		}
		else {
			push(@fas, $from_auths);
		}
		if ($cites_auths =~ m/;/) {
#@cas = split(/; /, $cites_auths);
			@cas = @{aan::extract_authors($cites_auths)};
		}
		else {	
			push(@cas, $cites_auths);
		}
		foreach my $fa (@fas) {
			foreach my $ca (@cas) {
				if($fa ne "" && $ca ne "") {
					if (!$nonself || !($fa eq  $ca))
					{
						$incites{$ca}++;
						$outcites{$fa}++;
					}
				}
			}
		}
	 }
	}
}
my $key;

if($incites)
{
	foreach $key (sort (keys(%incites))) {
		if($key ne "") {	
		   	print "$incites{$key}\t$key\n";}
		}
}
if($outcites)
{
	foreach $key (sort (keys(%outcites))) {
		if($key ne "")
		{
			  print "$outcites{$key}\t$key\n";
		}
	}
}


sub usage
{
		print "Usage: $0 [-release=release_year] [-year=to_year] [-incites] [-outcites] [-nonself] [-help]\n";
		print "\t-release=release_year\n";
		print "\t\tCan be any one of 2008, 2009, 2010 or 2011, defaults to 2011.\n";
		print "\t-year=to_year\n";
		print "\t\twhen specified, only citations which are older than the year mentioned are included. Can be any year greater than 1965, defaults to 2011.\n";
		print "\t-incites\n";
		print "\t\tprints out the number of incoming citations for every author in the author citation network. By default it prints out the number of incoming citations.\n";
		print "\t-outcites\n";
		print "\t\tprints out the number of outgoing citations for every author in the author citation network\n";
		print "\t-nonself\n";
		print "\t\twhen specified, self citations are excluded. By default self citations are NOT excluded.\n";
		print "\t-help\n";
		print "\t\tprints out the different options available\n";
}



