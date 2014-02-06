from IPython.core.magic import (Magics,register_cell_magic, magics_class, line_magic, cell_magic, line_cell_magic)

found_venture_ripl = 0

try: 
    from venture.shortcuts import *
    ipy_ripl = make_church_prime_ripl()
    found_venture_ripl = 1
except:
    print 'failed to make venture ripl'
        

@magics_class
class VentureMagics2(Magics):

    def __init__(self, shell):
        super(VentureMagics2, self).__init__(shell)

    @line_cell_magic
    def v(self, line, cell=None):
        '''VentureMagics creates a RIPL on IPython startupt called ipy_ripl.
        You can use the RIPL via Python:
           ipy_ripl.assume('coin','(beta 1 1)')
        
        You can also use the RIPL via magic commands. Use %vl for single
        lines:
           %v [ASSUME coin (beta 1 1)]

        This magic can take Python expansions:
           %l [ASSUME coin {np.random.beta(1,1)} ]

        Use the cell magic %%vl for multi-line input:
           %%v
           [ASSUME coin (beta 1 1)]
           [ASSUME x (flip coin)]'''

        def directive_summary(directive):
            'returns summary of directive and its current value'
            ins = directive['instruction']
            d=''

            if ins == 'assume':
                if 'symbol' in directive:
                    d = '%s %s   =  %s' % (ins, directive['symbol'], directive['value'])
            elif ins == 'observe':
                if isinstance(directive['expression'],str):  # [observe x value]
                    d = '%s %s   =  %s' % (ins, directive['expression'], directive['value'])
                elif isinstance(directive['expression'],list):  # [observe (+ 1 x) value]
                    d = '%s (%s ... )    =  %s' % (ins, directive['expression'][0], directive['value'])
            elif ins == 'predict':
                if isinstance(directive['expression'],str): # [predict x] = value
                    d = '%s %s  =  %s' % (ins, directive['expression'],directive['value'])
                elif isinstance(directive['expression'],dict):  # [predict 10] = 10
                    d = '%s %s  =  %s' % (ins,directive['value'], directive['value'])
                elif isinstance(directive['expression'],list):
                    d = '%s (%s ... )   =  %s' % (ins, directive['expression'][0], directive['value'])

            return '[directive_id: %s].  %s ' % (directive['directive_id'], d)
            

        ## FIXME:
        # Need to make things work after ipython %reset
        # recreate ipy_ripl in case of %reset
        # try:
        #     ipy_ripl.__doc__
        # except:
        #     try:
        #         from venture.shortcuts import make_church_prime_ripl
        #         ipy_ripl = make_church_prime_ripl()
        #     except:
        #         print 'failed to make venture ripl'

        

        ## LINE MAGIC
        if cell is None:
            
            venture_outs = ipy_ripl.execute_instruction( str(line), params=None )

            directives = ipy_ripl.list_directives()

            if directives: # if non-empty, print last directive added
                print directive_summary( ipy_ripl.list_directives()[-1] )
                value = ipy_ripl.list_directives()[-1]['value']
            else:
                value = None

            return value,venture_outs
            
        ## CELL MAGIC    
        else:
            old_directives = ipy_ripl.list_directives()

            venture_outs = ipy_ripl.execute_program( str(cell), params=None )

            new_directives = ipy_ripl.list_directives()

            diff = [d for d in new_directives if d not in old_directives]

            # diff is slow, speed up by assuming no [CLEAR] directive
            # diff  = ipy_ripl.list_directives()[ len(old_directives) :]

            values = []
            
            for directive in diff:
                print directive_summary(directive)
                values.append(directive['value'])

            return values,venture_outs
    
    
    
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(VentureMagics2)
    if found_venture_ripl==1: 
        print 'loaded VentureMagics2 with ripl "ipy_ripl"'
    
try:
    ip = get_ipython()
    load_ipython_extension(ip)

except:
    print 'ip=get_ipython() didnt run'   


