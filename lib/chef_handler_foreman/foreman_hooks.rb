require 'chef_handler_foreman/foreman_facts'
require 'chef_handler_foreman/foreman_reporting'

# this reporter is supported in chef 11 or later
unless Gem::Version.new(Chef::VERSION) < Gem::Version.new('11.0.0')
  require 'chef_handler_foreman/foreman_resource_reporter'
end

require 'chef_handler_foreman/foreman_uploader'

module ChefHandlerForeman
  module ForemanHooks
    # {:url => '', ...}
    def foreman_server_options(options)
      options = { :client_key => client_key || '/etc/chef/client.pem' }.merge(options)
      @foreman_uploader = ForemanUploader.new(options)
      # set uploader if handlers are already created
      @foreman_facts_handler.uploader = @foreman_uploader if @foreman_facts_handler
      @foreman_report_handler.uploader = @foreman_uploader if @foreman_report_handler
      @foreman_reporter.uploader = @foreman_uploader if @foreman_reporter
    end

    def foreman_facts_upload(upload, options = {})
      if upload
        @foreman_facts_handler = ForemanFacts.new({
          :uploader  => @foreman_uploader,
        }.merge(options))
        report_handlers << @foreman_facts_handler
        exception_handlers << @foreman_facts_handler
      end
    end

    def foreman_reports_upload(upload, *args)
      if upload
        mode = args.first.is_a?(Fixnum) ? args.shift : 1
        options = args.shift || {}
        mode = options[:mode] if options[:mode]
        case mode
          when 1
            @foreman_reporter = ForemanResourceReporter.new({
              :uploader  => @foreman_uploader,
              :log_level => @foreman_reports_log_level,
            }.merge(options))
            if Chef::Config[:event_handlers].is_a?(Array)
              Chef::Config[:event_handlers].push @foreman_reporter
            else
              Chef::Config[:event_handlers] = [@foreman_reporter]
            end
          when 2
            @foreman_report_handler = ForemanReporting.new({
              :uploader  => @foreman_uploader,
            }.merge(options))
            report_handlers << @foreman_report_handler
            exception_handlers << @foreman_report_handler
          else
            raise ArgumentError, 'unknown mode: ' + mode.to_s
        end
      end
    end

    # level can be string error notice debug
    def reports_log_level(level)
      raise ArgumentError, 'unknown level: ' + level.to_s unless %w(error notice debug).include?(level)

      @foreman_reports_log_level = level
      if @foreman_reporter
        @foreman_reporter.log_level = level
      end
    end
  end
end
