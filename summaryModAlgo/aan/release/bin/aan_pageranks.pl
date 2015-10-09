#!/usr/local/bin/perl

use strict;
use Clair::Network;
use Getopt::Long;

my $input = '';
my $fname = '';
my $release = 2013;
my $help = 0;

my $res = GetOptions("release:i" => \$release,
				"input=s" => \$input,
				"help" => \$help);

if(($input ne "acit" && $input ne "pcit") ||$help)
{
		usage();
		exit;
}
if($input eq "acit")
{
		$fname = "../release/$release/networks/author-citation-network.txt";
}

else
{
		$fname = "../release/$release/acl.txt";
}


open NETWORK_FILE, $fname or die "Cannot open the network $fname\n";

my @edges = <NETWORK_FILE>;

#print "Creating network\n";
my $network = new Clair::Network();
foreach my $edge (@edges) {
		my @nodes = split(" ==> ", $edge);
		print "Adding edge between $nodes[0] and $nodes[1]\n";
if($nodes[0] ne $nodes[1]) {
		$network->add_edge($nodes[0], $nodes[1]);
		$network->set_edge_attribute($nodes[0], $nodes[1], 'pagerank_transition', 1.0);
}
}

### Compute the PageRank for the network, save the distribution
$network->compute_pagerank();
my $pagerank_file = "./pageranks.txt";
$network->save_current_pagerank_distribution($pagerank_file);


sub usage {
		print "Usage: $0 -input=[\"acit\"|\"pcit\"] [-help]\n";
		print "\t--input=\"acit\"|\"pcit\"\n";
		print "\t\tInput network\n";
}


