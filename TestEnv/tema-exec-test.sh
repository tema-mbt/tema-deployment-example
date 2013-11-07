#!/bin/bash
set -e

echo "Using model package: $1"
echo "Adapter to call: $2"

MODEL_HAS_PARAMS=YES
USE_REAL_ADAPTER=YES
ADAPTER_CMD=$2

if [ "x$ADAPTER_CMD" == "x" ] ; then
    USE_REAL_ADAPTER=NO
fi

TESTDEF=tema_test.batch
MODEL_PAR_DEF=param_definitions.lst
RM="rm -rf"

for ent in Model testiconffi.conf engine.prms TestModel "$TESTDEF" "$MODEL_PAR_DEF"
do
    test -e "$ent" && $RM $ent
done

if [ "x$1" == "x--clean" ] ; then
    exit 0
fi

# If model parameters have to be defined
# ... This is model package dependent!
if [ "x$MODEL_HAS_PARAMS" == "xYES" ] ; then
    cat > "$MODEL_PAR_DEF" <<END
Color, cX, cY, R: (("red", 150, 100, 70), ("yellow", 200, 250, 100))
END
fi
#, ("yellow", 200, 250, 100)

# Parameters for test execution
#... test target definition. This is model package dependent!
cat > "$TESTDEF" <<END
Ruut;Symbols;Events
END

#... test generation parameters
cat >> "$TESTDEF" <<END
--coveragereq=
--guidance=guiguidance
--adapter=guiadapter
--testdata=nodata
END

if [ "x$MODEL_HAS_PARAMS" == "xYES" ] ; then
    echo "--modelvardefs=./$MODEL_PAR_DEF" >> "$TESTDEF"
fi

# Modification: for simulation with data
sed -i -e '/^.*nodata.*/d' "$TESTDEF"

# Modification: executing key words in real test target
# Un-comment the following line and test generator will wait connection
# from real adapter for test execution.
if [ "x$USE_REAL_ADAPTER" == "xYES" ] ; then
    sed -i -e '/^--adapter=gui.*/d' "$TESTDEF"
fi

# Execution of defined test
if [ "x$USE_REAL_ADAPTER" == "xYES" ] ; then
    /bin/bash -c "( cat \"$TESTDEF\" | tema batch --exec \"$1\" )" < /dev/null &
    sleep 20
    $ADAPTER_CMD -a localhost -p 9090 $3
else
    cat "$TESTDEF" | tema batch --exec "$1"
fi
