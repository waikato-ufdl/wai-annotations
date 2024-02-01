#!/bin/bash
#
# Script to install all the wai.annotations repos in a virtual environment

# the usage of this script
function usage()
{
   echo
   echo "${0##*/} [-v <dir>] [-p <path>] [-y] [-l] [-o] [-h]"
   echo
   echo "Installs all the wai.annotations repos in a virtual environment."
   echo
   echo " -h   this help"
   echo " -v   <dir>"
   echo "      the virtual environment directory to use, default: $VENV_DIR_DEFAULT"
   echo " -p   <path>"
   echo "      the path to the Python interpreter to use, default: $PYTHON_INTERPRETER_DEFAULT"
   echo " -y   whether to assume 'yes' for user prompts, "
   echo "      e.g., if the venv dir already exists and requires deleting"
   echo " -l   whether to install the latest, i.e., straight from the github repositories"
   echo "      rather than using the modules published on PyPI.org."
   echo " -o   when installing latest ('-l') also installs the optional modules like wai.annotations.tf."
   echo
}

VENV_DIR_DEFAULT="./venv"
VENV_DIR=$VENV_DIR_DEFAULT
PYTHON_INTERPRETER_DEFAULT="/usr/bin/python3"
PYTHON_INTERPRETER=$PYTHON_INTERPRETER_DEFAULT
ASSUME_YES="no"
LATEST="no"
OPTIONAL="no"

# interpret parameters
while getopts ":hylov:p:" flag
do
   case $flag in
      v) VENV_DIR=$OPTARG
         ;;
      p) PYTHON_INTERPRETER=$OPTARG
         ;;
      y) ASSUME_YES="yes"
         ;;
      l) LATEST="yes"
         ;;
      o) OPTIONAL="yes"
         ;;
      h) usage
         exit 0
         ;;
      *) usage
         exit 1
         ;;
   esac
done

echo
echo "wai.annotations installation"
echo "============================"

# delete venv dir
if [ -d "$VENV_DIR" ]
then
  if [ ! "$ASSUME_YES" = "yes" ]
  then
    echo
    read -n 1 -p "Virtual environment '$VENV_DIR' exists - remove (y/n)? " ANSWER
    if [ "$ANSWER" != "y" ]
    then
      echo
      echo "Keeping the virtual environment, exiting script."
      echo
      exit 0
    else
      echo
    fi
  fi
  echo
  echo "Deleting virtual environment: $VENV_DIR"
  rm -R "$VENV_DIR"
fi

PIP="$VENV_DIR/bin/pip"

# create venv
echo
echo "Creating virtual environment: $VENV_DIR"
echo
$PYTHON_INTERPRETER -m venv "$VENV_DIR"

# update tools
"$VENV_DIR/bin/pip" install wheel

# installing wai.annotation
echo
echo "Installing wai.annotations modules..."
echo
if [ "$LATEST" = "yes" ]
then
  OPTIONAL_PIP=""
  if [ "$OPTIONAL" = "yes" ]
  then
    OPTIONAL_PIP="git+https://github.com/waikato-ufdl/wai-annotations-tf.git"
  fi
  "$PIP" install "numpy<1.23.0" pipdeptree "pillow<9" "scikit-image<0.20.0"
  "$PIP" install wai.pycocotools
  "$PIP" install \
      git+https://github.com/waikato-ufdl/wai-annotations-core.git \
      git+https://github.com/waikato-ufdl/wai-annotations-adams.git \
      git+https://github.com/waikato-ufdl/wai-annotations-audio.git \
      git+https://github.com/waikato-ufdl/wai-annotations-bluechannel.git \
      git+https://github.com/waikato-ufdl/wai-annotations-coco.git \
      git+https://github.com/waikato-ufdl/wai-annotations-commonvoice.git \
      git+https://github.com/waikato-ufdl/wai-annotations-coqui.git \
      git+https://github.com/waikato-ufdl/wai-annotations-festvox.git \
      git+https://github.com/waikato-ufdl/wai-annotations-generic.git \
      git+https://github.com/waikato-ufdl/wai-annotations-grayscale.git \
      git+https://github.com/waikato-ufdl/wai-annotations-imgaug.git \
      git+https://github.com/waikato-ufdl/wai-annotations-imgstats.git \
      git+https://github.com/waikato-ufdl/wai-annotations-imgvis.git \
      git+https://github.com/waikato-ufdl/wai-annotations-indexedpng.git \
      git+https://github.com/waikato-ufdl/wai-annotations-layersegments.git \
      git+https://github.com/waikato-ufdl/wai-annotations-opex.git \
      git+https://github.com/waikato-ufdl/wai-annotations-redis-predictions.git \
      git+https://github.com/waikato-ufdl/wai-annotations-roi.git \
      git+https://github.com/waikato-ufdl/wai-annotations-subdir.git \
      $OPTIONAL_PIP \
      git+https://github.com/waikato-ufdl/wai-annotations-vgg.git \
      git+https://github.com/waikato-ufdl/wai-annotations-video.git \
      git+https://github.com/waikato-ufdl/wai-annotations-voc.git \
      git+https://github.com/waikato-ufdl/wai-annotations-yolo.git
else
  "$PIP" install "numpy<1.23.0" "pillow<9" "scikit-image<0.20.0"
  "$PIP" install wai.pycocotools
  "$PIP" install wai.annotations
fi

# done
WAIANN="$VENV_DIR/bin/wai-annotations"
if [ -f "$WAIANN" ]
then
  echo
  echo "Installation finished!"
  echo
  echo "You can now use wai.annotations directly as follows:"
  echo "  $WAIANN [options]"
  echo
  echo "Or you can activate the virtual environment using this command:"
  echo "  . $VENV_DIR/bin/activate"
  echo
  echo "And then deactivate it again with this command:"
  echo "  deactivate"
  echo
else
  echo
  echo "Installation failed, check console output!"
  echo
fi
