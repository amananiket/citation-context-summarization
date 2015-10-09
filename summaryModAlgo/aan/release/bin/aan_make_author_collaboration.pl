#!/usr/local/bin/perl

use aan;
use strict;
use Getopt::Long;


my $metafile = '';
my $to_year = 2011;
my $release = 2011;
my $help = 0;
GetOptions("release:i" => \$release,
		   "year:i" => \$to_year,
		   "help" => \$help);

if($help)
{
		usage();
		exit;
}

$metafile = "../$release/acl-metadata.txt";

my %meta = aan::buildmeta($metafile);



my @collabs = ();
foreach my $id ( keys %meta ) {
	if(&aan::select_year($id,$to_year) == 1) {
	my $value = $meta{$id};
	$value =~ s/ ::: .+//;
	if ($value =~ m/ :: /) {
		my @chunks = split(/ :: /, $value);
		push(@collabs, @chunks);
	}
	else {
		push(@collabs, $value);
	}
  }
}
foreach my $collab (@collabs) {
	if ($collab =~ m/; /) {
#my @auths = split(/; /, $collab);
		my @auths = @{aan::extract_authors($collab)};
		foreach my $auth1 (@auths) {
			if($auth1 eq "")
			{	
					next;
			}
			foreach my $auth2 (@auths) {
					if($auth2 eq "")
					{
							next;
					}
					if ($auth1 ne $auth2) {
							print "$auth1 ==> $auth2\n";
					}
			}
		}
	}
}

sub usage
{
		print "Usage: $0 [-release=release_year] [-year=to_year] [-help]\n";
		print "\t-release=release_year\n";
		print "\t\tCan be any one of 2008, 2009, 2010 or 2011, defaults to 2011.\n";
		print "\t-year=to_year\n";
		print "\t\twhen specified, only citations which are older than the year mentioned are included. Can be any year greater than 1965, defaults to 2011.\n";
		print "\t-help\n";
		print "\t\tprints out the different options available\n";
}

