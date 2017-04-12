from vcr import VCR


vcr = VCR(
    cassette_library_dir='resources/cassettes',
    path_transformer=VCR.ensure_suffix('.yaml'),
    filter_headers=['authorization'],
    record_mode='once',
    match_on=['method', 'path', 'query'],
)
