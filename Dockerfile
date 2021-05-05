
FROM golang:1.15 as builder
WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod vendor
COPY . .
RUN make vendor linux

FROM registry.opensource.zalan.do/library/alpine-3.12:latest
LABEL maintainer="Team ACID @ Zalando <team-acid@zalando.de>"

# We need root certificates to deal with teams api over https
RUN apk --no-cache add curl
RUN apk --no-cache add ca-certificates

COPY --from=builder /app/build/linux/postgres-operator /

RUN addgroup -g 1000 pgo
RUN adduser -D -u 1000 -G pgo -g 'Postgres Operator' pgo

USER 1000:1000

ENTRYPOINT ["/postgres-operator"]
