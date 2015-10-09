#!/usr/local/bin/perl


use aan;
use strict;
use Getopt::Long;


my $metafile = '';
my $acl_file = '';

my $incites_flag = 1;
my $outcites_flag = 0;
my $release = 2012;
my $to_year = 2012;
my $nonself = 0;
my $help = 0;

GetOptions("release:i" => \$release,
		   "incites" => \$incites_flag,
		   "outcites" => \$outcites_flag,
		   "year:i" => \$to_year,
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

open (IN, $acl_file) || die ("Could not open network.\n");
chomp (my @network = <IN>);
close IN;
my %incites = '';
my %outcites = '';


foreach my $paper_id (keys (%meta)) {
		if(&aan::select_year($paper_id,$to_year) == 1) {
			$incites{$paper_id} = 0;
			$outcites{$paper_id} = 0;
		}
}


foreach my $pair (@network) {
		$pair =~ /(.+) ==> (.+)/;
	my ($from, $cites) = ($1, $2);
	if(&aan::select_year($from,$to_year) == 1 && &aan::select_year($from,$to_year) == 1)
	{
		if(!$nonself || (&isSelfCitation($from,$cites) == 0))
		{
			$incites{$cites}++;
			$outcites{$from}++;
		}
	}
}


if($incites_flag == 1)
{

	foreach my $paper_id (sort (keys (%incites)))
	{
			my @attributes = split(/ ::: /,$meta{$paper_id});
			print "$incites{$paper_id}\t$paper_id\t$attributes[0]\t$attributes[1]\n";
	}
}
if ($outcites_flag == 1)
{

	foreach my $paper_id (sort (keys (%outcites)))
	{
			my @attributes = split(/ ::: /,$meta{$paper_id});
			print "$outcites{$paper_id}\t$paper_id\t$attributes[0]\t$attributes[1]\n";
	}
}


sub isSelfCitation {
		my ($from, $cites);
		$from = $_[0];
		$cites = $_[1];
#my %meta = $_[2];

		my $self = 0;
		if(! exists($meta{$from}))
		{
#print "$from not found\n";
				return 0;
		}
		if(! exists ($meta{$cites}))
		{
#print "$cites not found\n";
				return 0;

		}

		my $from_auths = $meta{$from};
		$from_auths =~ s/ ::: .+//;
		$from_auths =~ s/ :: /; /;
		my $cites_auths = $meta{$cites};
		$cites_auths =~ s/ ::: .+//;
		$cites_auths =~ s/ :: /; /;


		my (@fas, @cas);
		if (($from_auths ne "na") && ($cites_auths ne "na") && ($cites_auths ne "") && ($cites_auths ne "")) {
				if ($from_auths =~ m/;/) {
						@fas = split(/; /, $from_auths);
				}
				else {
						push(@fas, $from_auths);
				}
				if ($cites_auths =~ m/;/) {
						@cas = split(/; /, $cites_auths);
				}
				else {
						push(@cas, $cites_auths);
				}
				foreach my $fa (@fas) {
						foreach my $ca (@cas) {
								if($fa eq $ca)
								{
										$self = 1;
										last;
								}
						}
				}
		}
		$self;
}


sub usage
{
		print "Usage: $0 [-release=release_year] [-year=to_year] [-incites] [-outcites] [-nonself] [-help]\n";
		print "\t-release=release_year\n";
		print "\t\tCan be any one of 2008, 2009, 2010 or 2011, defaults to 2011.\n";
		print "\t-year=to_year\n";
		print "\t\twhen specified, only citations which are older than the year mentioned are included. Can be any year greater than 1965, defaults to 2011.\n";
		print "\t-incites\n";
		print "\t\tprints out the number of incoming citations for every paper in the paper citation network. By default it prints out the number of incoming citations.\n";
		print "\t-outcites\n";
		print "\t\tprints out the number of outgoing citations for every paper in the paper citation network\n";
		print "\t-nonself\n";
		print "\t\twhen specified, self citations are excluded. By default self citations are NOT excluded.\n";
		print "\t-help\n";
		print "\t\tprints out the different options available\n";
}

