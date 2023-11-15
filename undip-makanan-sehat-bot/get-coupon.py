import argparse
import getpass


parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawTextHelpFormatter,
                    prog='./get-coupon.py',
                    description='''Example:
python get-coupon.py -e "jeff@students.undip.ac.id" -p "jeff123" -l 1''',
                    epilog='-Raft')

locHelpText = '''location index (int):
1 - Student Center
2 - Halaman Parkir Gedung SA-MWA
3 - Auditorium FPIK
4 - Auditorium Imam Bardjo, S.H.'''

parser.add_argument("-e", "--email" , type=str, metavar='', help="email (students.undip.ac.id)")
parser.add_argument("-p", "--pw"    , type=str, metavar='', help="password")
parser.add_argument("-l", "--loc"   , type=int, metavar='', help=locHelpText)
parser.add_argument("-d", "--delay" , type=float, metavar='', help="form page refresh delay")
parser.add_argument("-S", "--Sentry", type=float, metavar='', help="Activates sentry mode with determined time interval")
parser.add_argument("-s", "--save"  , action='store_true', help="save coupon as PNG image")
parser.add_argument("-t", "--test"  , action='store_true', help="test program")
 
args = parser.parse_args()

email = args.email
pw = args.pw
locIndex = args.loc if not args.test else 1
delay = args.delay or 0
interval = args.Sentry or 0

if not (email and pw and locIndex):
    print("[SYS] Incomplete argument, please complete the following:")
    if not email:
        email = input("      Email: ")
    if not pw:
        pw = getpass.getpass(prompt="      Password: ")
    if (not locIndex):
        locIndex = input("""\n      Locations:
      1 - Student Center
      2 - Halaman Parkir Gedung SA-MWA
      3 - Auditorium FPIK
      4 - Auditorium Imam Bardjo, S.H.
      Choose location (1-4): """)
        
print('\033[93m' + '''
[]==========================[WARNING]==========================[]
Check system clock accuracy by visiting https://time.is/

If your system clock is AHEAD, add a delay accordingly with the -d flag
[]=============================================================[]
''' + '\033[0m' )

from helper.helper import FoodTruckHelper

bot  = FoodTruckHelper(email, pw, locIndex, delay, interval)

bot.login()
bot.navigate()

if args.test:
    bot.getCouponTest()
    if args.save:
        print("[SYS] Coupon image can't be generated during test")
else:
    if args.Sentry:
        bot.GetCouponSentry()
    else:
        bot.getCoupon()
    if args.save:
        bot.getScreenshot()
