import unittest
from pyNastran.dev.solver.solver import Solver, BDF, CaseControlDeck


class TestSolverSprings(unittest.TestCase):
    def test_celas1(self):
        model = BDF(debug=True, log=None, mode='msc')
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [0., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        model.add_celas1(eid, pid, nids, c1=1, c2=1, comment='')
        k = 1000.

        load_id = 2
        spc_id = 3
        model.add_pelas(pid, k, ge=0., s=0., comment='')
        model.add_sload(load_id, 2, 20.)
        lines = [
            'STRESS(PLOT,PRINT) = ALL',
            'STRAIN(PLOT,PRINT) = ALL',
            'FORCE(PLOT,PRINT) = ALL',
            'DISP(PLOT,PRINT) = ALL',
            'GPFORCE(PLOT,PRINT) = ALL',
            'SPCFORCE(PLOT,PRINT) = ALL',
            'SUBCASE 1',
            '  LOAD = 2',
            '  SPC = 3',
        ]
        cc = CaseControlDeck(lines, log=model.log)
        model.sol = 101
        model.case_control_deck = cc

        solver = Solver(model)
        solver.run()

    def test_conrod(self):
        model = BDF(debug=True, log=None, mode='msc')
        model.add_grid(1, [0., 0., 0.])
        model.add_grid(2, [1., 0., 0.])
        nids = [1, 2]
        eid = 1
        pid = 2
        mid = 3
        E = 3.0e7
        G = None
        nu = 0.3
        model.add_mat1(mid, E, G, nu, rho=0.0, a=0.0, tref=0.0, ge=0.0, St=0.0,
                       Sc=0.0, Ss=0.0, mcsid=0)
        model.add_conrod(eid, mid, nids, A=1.0, j=2.0, c=0.0, nsm=0.0)

        load_id = 2
        spc_id = 3
        nid = 2
        mag = 1,
        fxyz = [1., 0., 0.]
        model.add_force(load_id, nid, mag, fxyz, cid=0)
        lines = [
            'STRESS(PLOT,PRINT) = ALL',
            'STRAIN(PLOT,PRINT) = ALL',
            'FORCE(PLOT,PRINT) = ALL',
            'DISP(PLOT,PRINT) = ALL',
            'GPFORCE(PLOT,PRINT) = ALL',
            'SPCFORCE(PLOT,PRINT) = ALL',
            'SUBCASE 1',
            '  LOAD = 2',
            '  SPC = 3',
        ]
        cc = CaseControlDeck(lines, log=model.log)
        model.sol = 101
        model.case_control_deck = cc

        solver = Solver(model)
        solver.run()

if __name__ == '__main__':
    unittest.main()
