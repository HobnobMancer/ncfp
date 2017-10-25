#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Functions to interact with Entrez

(c) The James Hutton Institute 2017
Author: Leighton Pritchard

Contact: leighton.pritchard@hutton.ac.uk
Leighton Pritchard,
Information and Computing Sciences,
James Hutton Institute,
Errol Road,
Invergowrie,
Dundee,
DD6 9LH,
Scotland,
UK

The MIT License

Copyright (c) 2017 The James Hutton Institute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from io import StringIO

from Bio import Entrez
from tqdm import tqdm

from .ncfp_tools import last_exception

# EXCEPTIONS
# ==========
class NCFPELinkException(Exception):
    """Exception for ELink qeries."""

    def __init__(self, msg="Error in ncfp ELink query"):
        """Instantiate class."""
        Exception.__init__(self, msg)


class NCFPEFetchException(Exception):
    """Exception for EFetch queries."""

    def __init__(self, msg="Error in ncfp EFetch query"):
        """Instantiate class."""
        Exception.__init__(self, msg)


class NCFPESearchException(Exception):
    """Exception for ESearch queries."""

    def __init__(self, msg="Error in ncfp ESearch query"):
        """Instantiate class."""
        Exception.__init__(self, msg)


class NCFPMaxretryException(Exception):
    """Exception raised when maximum retries are reached"""

    def __init__(self, msg="Maximum retries exceeded"):
        """Instantiate class."""
        Exception.__init__(self, msg)


def fetch_gb_headers(records, cache, retries):
    """Returns NCBI GenBank headers for passed records

    records - collection of SeqRecords
    retries - number of Entrez retries
    """
    # Collate all unique nucleotide accessions
    accessions = set()
    for record in tqdm(records, desc="Collating accessions"):
        for acc in record.ncfp['nt_acc']:
            accessions.add(acc)

    # Check accessions against those in the cache. We only
    # retrieve accessions not in the cache
    fetchlist = accessions.difference(set(cache.keys()))
            
    # Get GenBank header for each unique accession
    for accession in tqdm(fetchlist, desc="Fetch GenBank headers"):
        try:
            retval = efetch_with_retries(accession,
                                         'nucleotide', 'gb', 'text',
                                         retries).read().strip()
        except NCFPMaxretryException:
            continue
    return cache


# Query NCBI singly with each record, to recover nucleotide accessions
def search_nt_ids(records, cache, retries):
    """Returns records with NCBI nucleotide ID as an attribute.

    records - collection of SeqRecords
    cache   - accession cache (dictionary)
    retries - number of Entrez retries

    Passed records must have the record.ncfp attribute. This will
    be extended with the ['nt_accession'] key, whose value is the
    NCBI accession for that sequence.

    If the record's ID is in the cache, the ESearch is not
    performed - the cache is presumed to be up to date.
    """
    successrecords = []
    failrecords = []
    for record in tqdm(records, desc="Search NT IDs"):
        if record.ncfp['nt_query'] not in cache:
            try:
                result = esearch_with_retries(record.ncfp['nt_query'],
                                              'nucleotide', retries)
            except NCFPESearchException:
                failrecords.append(record)
            if int(result['Count']) == 0:
                failrecords.append(record)
            else:
                successrecords.append(record)
                record.ncfp['nt_acc'] = result['IdList']
                cache[record.ncfp['nt_query']] = result['IdList']
        else:
            record.ncfp['nt_acc'] = cache[record.ncfp['nt_query']]
            successrecords.append(record)
    return successrecords, cache, failrecords


# Run an ESearch on a single ID
def esearch_with_retries(query_id, dbname, maxretries):
    """Entrez ESearch for single query ID.

    query_id    - query term for search
    dbname      - NCBI target database name
    maxretries  - maximum number of attempts to make

    Returns the parsed record resulting from the ESearch,
    after trying the ESearch up to a maximum number of times.
    """
    tries = 0
    while tries < maxretries:
        try:
            handle = Entrez.esearch(db=dbname, term=query_id)
            return Entrez.read(handle)
        except:
            tries += 1
    raise NCFPMaxretryException("Query ID %s ESearch failed" % query_id)


# Run an EFetch on a single ID
def efetch_with_retries(query_id, dbname, rettype, retmode, maxretries):
    """Entrez EFetch for a single query ID.

    query_id      - query term for search
    dbname        - NCBI target database name
    rettype       - requested return type
    retmode       - format of data to be returned
    maxretries    - maximum number of attempts to make

    Returns a handle to a completely buffered string, after a read()
    operation, sanity check, and retokenising.
    """
    tries = 0
    while tries < maxretries:
        try:
            data = Entrez.efetch(db=dbname, rettype=rettype,
                                 retmode=retmode,
                                 id=query_id).read()
            if rettype in ['gb', 'gbwithparts'] and retmode == 'text':
                assert data.startswith('LOCUS')
            # Return data string as stream
            return StringIO(data)
        except:
            print(last_exception())
            tries += 1
    raise NCFPMaxretryException("Query ID %s EFetch failed" % query_id)


def set_entrez_email(email):
    """Sets Entrez email address."""
    Entrez.email = email
