from Face_Detector import detect_face
import sys
def main():
    if detect_face(sys.argv[1]):
        return "1"
    else:
        return "0"

if __name__ == "__main__":
    print(main())
