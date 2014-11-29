
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def display_report(runner):
    for result in runner.results:
        if not result['failed']:
            continue
        print "\n\n############################ FAILED ############################"
        for e in result['failed']:
            print bcolors.FAIL, result.get('name'), ":", e['name']
            print bcolors.ENDC
            for i, error in enumerate(e['errors']):
                print "%d." % i
                print error
                print
            print "-------- LOG OUTPUT --------"
            print e['logs']
            print "---------------------------"

    print "\n\n############################ RESULTS ############################"
    for result in runner.results:
        c = bcolors.OKGREEN
        if result.get('failed'):
            c = bcolors.FAIL

        print c, result.get('name'),
        for k in ['passed', 'failed', 'skipped']:
            print "%s: %d " % (k, len(result.get(k))),
        print bcolors.ENDC