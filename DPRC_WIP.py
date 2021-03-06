import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    t1w = create_key('anat/sub-{subject}_T1w')
    t2w = create_key('anat/sub-{subject}_T2w')
    flair = create_key('anat/sub-{subject}_flair')
    dwi = create_key('dwi/sub-{subject}_dwi')
    asl = create_key('asl/sub-{subject}_task-rest_asl')
    rest = create_key('func/sub-{subject}_task-rest_bold')
    rest_sbref = create_key('func/sub-{subject}_task-rest_sbref')
    info = {t1w: [], t2w: [], flair: [], dwi: [], asl:[], rest:[], rest_sbref:[]}
    # please note, I have made a asl folder, rather than put it in func folder
    # the BID convention for perfusion has not be finalised yet, check back later
    # link for BIDs working doc is in here http://bids.neuroimaging.io/bids_spec1.0.2.pdf
    # last_run = len(seqinfo) don't think need this
    #################
    
    for idx, s in enumerate(seqinfo):
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        # anatomy scans
        if (s.dim3 == 208) and (s.dim4 == 1) and ('T1' in s.protocol_name):
            info[t1w] = [s.series_id]
        if ('T2_BLADE' in s.protocol_name):
            info[t2w] = [s.series_id]
        if ('T2_FLAIR' in s.protocol_name):
            info[flair] = [s.series_id]
        # diffusion scans
        if (s.dim4 == 105) and ('Diff' in s.protocol_name):
            info[dwi] = [s.series_id]
        # i need to add in here all the blip up and blip down scans
        # perfusion scan
        if (s.dim4 == 17) and ('pcasl' in s.protocol_name):
            info[asl] = [s.series_id]
        # functional scan
        if (s.dim4 == 490) and ('bold' in s.protocol_name):
            info[rest] = [s.series_id]
        if (s.dim4 == 1) and ('bold' in s.protocol_name):
            info[rest_sbref] = [s.series_id]
    return info
